from flask import Blueprint, request, jsonify
from database import execute_query, execute_insert, execute_update
from routes.auth import get_current_user, admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)."""
    users = execute_query(
        """SELECT id, nickname, nome, email, role, status, created_at
           FROM users
           ORDER BY created_at DESC"""
    )
    
    return jsonify({'users': users or []})


@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])
@admin_required
def ban_user(user_id):
    """Ban a user (admin only)."""
    admin = get_current_user()
    data = request.get_json()
    
    reason = data.get('reason', '').strip()
    
    # Check user exists
    user = execute_query(
        "SELECT id, status, role FROM users WHERE id = %s",
        (user_id,),
        fetchone=True
    )
    
    if not user:
        return jsonify({'error': 'Utente non trovato'}), 404
    
    if user['role'] == 'ADMIN':
        return jsonify({'error': 'Non puoi bannare un amministratore'}), 400
    
    if user['status'] == 'BANNED':
        return jsonify({'error': 'Utente già bannato'}), 400
    
    # Update user status
    execute_update("UPDATE users SET status = 'BANNED' WHERE id = %s", (user_id,))
    
    # Record ban
    execute_insert(
        """INSERT INTO user_bans (user_id, admin_id, reason, created_at)
           VALUES (%s, %s, %s, NOW())""",
        (user_id, admin['id'], reason)
    )
    
    return jsonify({'message': 'Utente bannato'})


@admin_bp.route('/users/<int:user_id>/unban', methods=['POST'])
@admin_required
def unban_user(user_id):
    """Unban a user (admin only)."""
    # Check user exists
    user = execute_query(
        "SELECT id, status FROM users WHERE id = %s",
        (user_id,),
        fetchone=True
    )
    
    if not user:
        return jsonify({'error': 'Utente non trovato'}), 404
    
    if user['status'] != 'BANNED':
        return jsonify({'error': 'Utente non bannato'}), 400
    
    # Update user status
    execute_update("UPDATE users SET status = 'ACTIVE' WHERE id = %s", (user_id,))
    
    # Update ban record
    execute_update(
        "UPDATE user_bans SET revoked_at = NOW() WHERE user_id = %s AND revoked_at IS NULL",
        (user_id,)
    )
    
    return jsonify({'message': 'Utente riabilitato'})


@admin_bp.route('/posts/<int:post_id>/moderate', methods=['POST'])
@admin_required
def moderate_post(post_id):
    """Moderate (soft delete) a post (admin only)."""
    # Check post exists
    post = execute_query(
        "SELECT id FROM posts WHERE id = %s AND deleted_at IS NULL",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    # Soft delete
    execute_update("UPDATE posts SET deleted_at = NOW() WHERE id = %s", (post_id,))
    execute_update("UPDATE commenti SET deleted_at = NOW() WHERE post_id = %s", (post_id,))
    
    return jsonify({'message': 'Post rimosso'})


@admin_bp.route('/comments/<int:comment_id>/moderate', methods=['POST'])
@admin_required
def moderate_comment(comment_id):
    """Moderate (soft delete) a comment (admin only)."""
    # Check comment exists
    comment = execute_query(
        "SELECT id FROM commenti WHERE id = %s AND deleted_at IS NULL",
        (comment_id,),
        fetchone=True
    )
    
    if not comment:
        return jsonify({'error': 'Commento non trovato'}), 404
    
    # Soft delete
    execute_update("UPDATE commenti SET deleted_at = NOW() WHERE id = %s", (comment_id,))
    
    return jsonify({'message': 'Commento rimosso'})


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """Get platform statistics (admin only)."""
    total_users = execute_query(
        "SELECT COUNT(*) as count FROM users WHERE status = 'ACTIVE'",
        fetchone=True
    )
    
    total_posts = execute_query(
        "SELECT COUNT(*) as count FROM posts WHERE deleted_at IS NULL",
        fetchone=True
    )
    
    total_comments = execute_query(
        "SELECT COUNT(*) as count FROM commenti WHERE deleted_at IS NULL",
        fetchone=True
    )
    
    closed_posts = execute_query(
        "SELECT COUNT(*) as count FROM posts WHERE status = 'CLOSED' AND deleted_at IS NULL",
        fetchone=True
    )
    
    total_experts = execute_query(
        "SELECT COUNT(DISTINCT user_id) as count FROM user_category_stats WHERE is_expert = 1",
        fetchone=True
    )
    
    return jsonify({
        'total_users': total_users['count'] if total_users else 0,
        'total_posts': total_posts['count'] if total_posts else 0,
        'total_comments': total_comments['count'] if total_comments else 0,
        'closed_posts': closed_posts['count'] if closed_posts else 0,
        'total_experts': total_experts['count'] if total_experts else 0
    })
