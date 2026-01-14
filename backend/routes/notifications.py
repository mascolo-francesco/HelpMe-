from flask import Blueprint, jsonify
from database import execute_query, execute_update
from routes.auth import get_current_user, login_required

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('', methods=['GET'])
@login_required
def get_notifications():
    """Get notifications for current user."""
    user = get_current_user()
    
    notifications = execute_query(
        """SELECT n.id, n.tipo, n.messaggio, n.post_id, n.created_at, n.read_at,
                  p.titolo_post as post_titolo
           FROM notifications n
           LEFT JOIN posts p ON p.id = n.post_id
           WHERE n.user_id = %s
           ORDER BY n.created_at DESC
           LIMIT 50""",
        (user['id'],)
    )
    
    unread_count = execute_query(
        "SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND read_at IS NULL",
        (user['id'],),
        fetchone=True
    )
    
    return jsonify({
        'notifications': notifications or [],
        'unread_count': unread_count['count'] if unread_count else 0
    })


@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    """Mark a notification as read."""
    user = get_current_user()
    
    execute_update(
        "UPDATE notifications SET read_at = NOW() WHERE id = %s AND user_id = %s",
        (notification_id, user['id'])
    )
    
    return jsonify({'message': 'Notifica letta'})


@notifications_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_as_read():
    """Mark all notifications as read."""
    user = get_current_user()
    
    execute_update(
        "UPDATE notifications SET read_at = NOW() WHERE user_id = %s AND read_at IS NULL",
        (user['id'],)
    )
    
    return jsonify({'message': 'Tutte le notifiche lette'})
