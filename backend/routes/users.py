from flask import Blueprint, request, jsonify
from database import execute_query, execute_update
from routes.auth import get_current_user, login_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/me', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile with stats."""
    user = get_current_user()
    
    # Get user stats per category
    stats = execute_query(
        """SELECT c.id, c.nome as categoria, ucs.score, ucs.is_expert
           FROM user_category_stats ucs
           JOIN categorie c ON c.id = ucs.categoria_id
           WHERE ucs.user_id = %s
           ORDER BY ucs.score DESC""",
        (user['id'],)
    )
    
    # Get subscribed categories
    subscriptions = execute_query(
        """SELECT c.id, c.nome
           FROM category_subscriptions cs
           JOIN categorie c ON c.id = cs.categoria_id
           WHERE cs.user_id = %s""",
        (user['id'],)
    )
    
    # Count posts and comments
    post_count = execute_query(
        "SELECT COUNT(*) as count FROM posts WHERE autore_id = %s AND deleted_at IS NULL",
        (user['id'],),
        fetchone=True
    )
    
    comment_count = execute_query(
        "SELECT COUNT(*) as count FROM commenti WHERE autore_id = %s AND deleted_at IS NULL",
        (user['id'],),
        fetchone=True
    )
    
    return jsonify({
        'user': {
            'id': user['id'],
            'nickname': user['nickname'],
            'nome': user['nome'],
            'email': user['email'],
            'role': user['role']
        },
        'stats': stats or [],
        'subscriptions': subscriptions or [],
        'post_count': post_count['count'] if post_count else 0,
        'comment_count': comment_count['count'] if comment_count else 0
    })


@users_bp.route('/me', methods=['PUT'])
@login_required
def update_profile():
    """Update current user profile."""
    user = get_current_user()
    data = request.get_json()
    
    nome = data.get('nome', '').strip()
    
    if not nome:
        return jsonify({'error': 'Nome è obbligatorio'}), 400
    
    execute_update(
        "UPDATE users SET nome = %s WHERE id = %s",
        (nome, user['id'])
    )
    
    return jsonify({'message': 'Profilo aggiornato'})


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get public user profile."""
    user = execute_query(
        "SELECT id, nickname, nome, role, status, created_at FROM users WHERE id = %s",
        (user_id,),
        fetchone=True
    )
    
    if not user:
        return jsonify({'error': 'Utente non trovato'}), 404
    
    # Get user stats per category
    stats = execute_query(
        """SELECT c.nome as categoria, ucs.score, ucs.is_expert
           FROM user_category_stats ucs
           JOIN categorie c ON c.id = ucs.categoria_id
           WHERE ucs.user_id = %s
           ORDER BY ucs.score DESC""",
        (user_id,)
    )
    
    return jsonify({
        'user': user,
        'stats': stats or []
    })


@users_bp.route('/experts', methods=['GET'])
def get_experts():
    """Get list of experts."""
    category_id = request.args.get('category')
    
    if category_id:
        experts = execute_query(
            """SELECT u.id, u.nickname, u.nome, c.nome as categoria, ucs.score
               FROM user_category_stats ucs
               JOIN users u ON u.id = ucs.user_id
               JOIN categorie c ON c.id = ucs.categoria_id
               WHERE ucs.is_expert = 1 AND ucs.categoria_id = %s AND u.status = 'ACTIVE'
               ORDER BY ucs.score DESC
               LIMIT 20""",
            (category_id,)
        )
    else:
        experts = execute_query(
            """SELECT u.id, u.nickname, u.nome, c.nome as categoria, ucs.score
               FROM user_category_stats ucs
               JOIN users u ON u.id = ucs.user_id
               JOIN categorie c ON c.id = ucs.categoria_id
               WHERE ucs.is_expert = 1 AND u.status = 'ACTIVE'
               ORDER BY ucs.score DESC
               LIMIT 20"""
        )
    
    return jsonify({'experts': experts or []})
