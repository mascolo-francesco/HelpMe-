from flask import Blueprint, request, jsonify, current_app
from database import execute_query, execute_insert, execute_update
from routes.auth import get_current_user, login_required

votes_bp = Blueprint('votes', __name__)


def update_user_score(user_id, category_ids, vote_delta):
    """Update user score for categories and check expert status."""
    expert_threshold = current_app.config.get('EXPERT_THRESHOLD', 100)
    
    for cat_id in category_ids:
        # Check if stats exist
        stats = execute_query(
            "SELECT score FROM user_category_stats WHERE user_id = %s AND categoria_id = %s",
            (user_id, cat_id),
            fetchone=True
        )
        
        if stats:
            new_score = stats['score'] + vote_delta
            is_expert = 1 if new_score >= expert_threshold else 0
            execute_update(
                """UPDATE user_category_stats 
                   SET score = %s, is_expert = %s, updated_at = NOW() 
                   WHERE user_id = %s AND categoria_id = %s""",
                (new_score, is_expert, user_id, cat_id)
            )
        else:
            new_score = vote_delta
            is_expert = 1 if new_score >= expert_threshold else 0
            execute_insert(
                """INSERT INTO user_category_stats (user_id, categoria_id, score, is_expert, updated_at)
                   VALUES (%s, %s, %s, %s, NOW())""",
                (user_id, cat_id, new_score, is_expert)
            )


@votes_bp.route('/comment/<int:comment_id>', methods=['POST'])
@login_required
def vote_comment(comment_id):
    """Vote on a comment (upvote or downvote)."""
    user = get_current_user()
    data = request.get_json()
    
    value = data.get('value', 0)  # 1 for upvote, -1 for downvote, 0 to remove vote
    
    if value not in [-1, 0, 1]:
        return jsonify({'error': 'Valore voto non valido'}), 400
    
    # Get comment and post info
    comment = execute_query(
        """SELECT c.id, c.autore_id, c.post_id
           FROM commenti c
           WHERE c.id = %s AND c.deleted_at IS NULL""",
        (comment_id,),
        fetchone=True
    )
    
    if not comment:
        return jsonify({'error': 'Commento non trovato'}), 404
    
    # Can't vote on own comments
    if comment['autore_id'] == user['id']:
        return jsonify({'error': 'Non puoi votare i tuoi commenti'}), 400
    
    # Get categories for the post (to update user score)
    categories = execute_query(
        "SELECT categoria_id FROM post_categorie WHERE post_id = %s",
        (comment['post_id'],)
    )
    category_ids = [c['categoria_id'] for c in (categories or [])]
    
    # Check existing vote
    existing_vote = execute_query(
        "SELECT value FROM comment_votes WHERE comment_id = %s AND voter_id = %s",
        (comment_id, user['id']),
        fetchone=True
    )
    
    old_value = existing_vote['value'] if existing_vote else 0
    
    if value == 0:
        # Remove vote
        if existing_vote:
            execute_update(
                "DELETE FROM comment_votes WHERE comment_id = %s AND voter_id = %s",
                (comment_id, user['id'])
            )
            # Update comment author's score (reverse the old vote)
            update_user_score(comment['autore_id'], category_ids, -old_value)
    else:
        if existing_vote:
            if existing_vote['value'] == value:
                return jsonify({'message': 'Voto già registrato'})
            
            # Update existing vote
            execute_update(
                "UPDATE comment_votes SET value = %s, created_at = NOW() WHERE comment_id = %s AND voter_id = %s",
                (value, comment_id, user['id'])
            )
            # Update comment author's score (reverse old, apply new)
            update_user_score(comment['autore_id'], category_ids, value - old_value)
        else:
            # Insert new vote
            execute_insert(
                "INSERT INTO comment_votes (comment_id, voter_id, value, created_at) VALUES (%s, %s, %s, NOW())",
                (comment_id, user['id'], value)
            )
            # Update comment author's score
            update_user_score(comment['autore_id'], category_ids, value)
    
    # Get updated vote count
    vote_count = execute_query(
        "SELECT COALESCE(SUM(value), 0) as total FROM comment_votes WHERE comment_id = %s",
        (comment_id,),
        fetchone=True
    )
    
    return jsonify({
        'message': 'Voto registrato',
        'vote_total': vote_count['total'] if vote_count else 0,
        'my_vote': value
    })
