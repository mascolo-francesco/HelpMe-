from flask import Blueprint, request, jsonify, current_app
from database import execute_query, execute_insert, execute_update
from routes.auth import get_current_user, login_required

comments_bp = Blueprint('comments', __name__)


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


@comments_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post_comments(post_id):
    """Get all comments for a post."""
    # Check post exists
    post = execute_query(
        "SELECT id, solution_comment_id FROM posts WHERE id = %s AND deleted_at IS NULL",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    # Get all comments with vote counts
    comments = execute_query(
        """SELECT c.id, c.testo, c.data_inserimento, c.parent_comment_id,
                  u.id as autore_id, u.nickname as autore_nickname, u.nome as autore_nome,
                  COALESCE(SUM(cv.value), 0) as voto_totale,
                  (SELECT COUNT(*) FROM comment_votes WHERE comment_id = c.id AND value = 1) as upvotes,
                  (SELECT COUNT(*) FROM comment_votes WHERE comment_id = c.id AND value = -1) as downvotes
           FROM commenti c
           JOIN users u ON u.id = c.autore_id
           LEFT JOIN comment_votes cv ON cv.comment_id = c.id
           WHERE c.post_id = %s AND c.deleted_at IS NULL
           GROUP BY c.id
           ORDER BY c.data_inserimento ASC""",
        (post_id,)
    )
    
    # Check if authors are experts
    for comment in (comments or []):
        is_expert = execute_query(
            """SELECT 1 FROM user_category_stats ucs
               JOIN post_categorie pc ON pc.categoria_id = ucs.categoria_id
               WHERE ucs.user_id = %s AND pc.post_id = %s AND ucs.is_expert = 1
               LIMIT 1""",
            (comment['autore_id'], post_id),
            fetchone=True
        )
        comment['autore_is_expert'] = bool(is_expert)
        comment['is_solution'] = comment['id'] == post['solution_comment_id']
    
    # Get current user's votes
    current_user = get_current_user()
    user_votes = {}
    if current_user:
        votes = execute_query(
            """SELECT comment_id, value FROM comment_votes 
               WHERE voter_id = %s AND comment_id IN (SELECT id FROM commenti WHERE post_id = %s)""",
            (current_user['id'], post_id)
        )
        for v in (votes or []):
            user_votes[v['comment_id']] = v['value']
    
    # Attach user votes to comments
    for comment in (comments or []):
        comment['my_vote'] = user_votes.get(comment['id'], 0)
    
    return jsonify({'comments': comments or []})


@comments_bp.route('/post/<int:post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    """Create a new comment on a post."""
    user = get_current_user()
    
    # Check post exists and is open
    post = execute_query(
        "SELECT id, status FROM posts WHERE id = %s AND deleted_at IS NULL",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    if post['status'] == 'CLOSED':
        return jsonify({'error': 'Impossibile commentare un post chiuso'}), 400
    
    data = request.get_json()
    testo = data.get('testo', '').strip()
    parent_comment_id = data.get('parent_comment_id')
    media_urls = data.get('media', [])
    
    if not testo:
        return jsonify({'error': 'Testo del commento è obbligatorio'}), 400
    
    # Verify parent comment if specified
    if parent_comment_id:
        parent = execute_query(
            "SELECT id FROM commenti WHERE id = %s AND post_id = %s AND deleted_at IS NULL",
            (parent_comment_id, post_id),
            fetchone=True
        )
        if not parent:
            return jsonify({'error': 'Commento padre non trovato'}), 404
    
    # Create comment
    comment_id = execute_insert(
        """INSERT INTO commenti (post_id, autore_id, parent_comment_id, testo, data_inserimento)
           VALUES (%s, %s, %s, %s, NOW())""",
        (post_id, user['id'], parent_comment_id, testo)
    )
    
    # Add media
    for m in media_urls:
        execute_insert(
            "INSERT INTO comment_media (comment_id, tipo, url, created_at) VALUES (%s, %s, %s, NOW())",
            (comment_id, m.get('tipo', 'IMAGE'), m.get('url'))
        )
    
    return jsonify({'message': 'Commento aggiunto', 'comment_id': comment_id}), 201


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """Soft delete a comment."""
    user = get_current_user()
    
    # Check ownership
    comment = execute_query(
        "SELECT autore_id FROM commenti WHERE id = %s AND deleted_at IS NULL",
        (comment_id,),
        fetchone=True
    )
    
    if not comment:
        return jsonify({'error': 'Commento non trovato'}), 404
    
    if comment['autore_id'] != user['id'] and user['role'] != 'ADMIN':
        return jsonify({'error': 'Non autorizzato'}), 403
    
    execute_update("UPDATE commenti SET deleted_at = NOW() WHERE id = %s", (comment_id,))
    
    return jsonify({'message': 'Commento eliminato'})
