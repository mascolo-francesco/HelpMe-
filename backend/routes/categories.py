from flask import Blueprint, request, jsonify
from database import execute_query, execute_insert, execute_update
from routes.auth import get_current_user, login_required, admin_required

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all categories with post counts."""
    categories = execute_query(
        """SELECT c.id, c.nome, c.descrizione,
                  (SELECT COUNT(DISTINCT pc.post_id) 
                   FROM post_categorie pc 
                   JOIN posts p ON p.id = pc.post_id 
                   WHERE pc.categoria_id = c.id AND p.deleted_at IS NULL) as post_count
           FROM categorie c
           ORDER BY c.nome"""
    )
    
    return jsonify({'categories': categories or []})


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get category details."""
    category = execute_query(
        "SELECT id, nome, descrizione FROM categorie WHERE id = %s",
        (category_id,),
        fetchone=True
    )
    
    if not category:
        return jsonify({'error': 'Categoria non trovata'}), 404
    
    # Get experts for this category
    experts = execute_query(
        """SELECT u.id, u.nickname, u.nome, ucs.score
           FROM user_category_stats ucs
           JOIN users u ON u.id = ucs.user_id
           WHERE ucs.categoria_id = %s AND ucs.is_expert = 1 AND u.status = 'ACTIVE'
           ORDER BY ucs.score DESC
           LIMIT 10""",
        (category_id,)
    )
    
    category['experts'] = experts or []
    
    return jsonify({'category': category})


@categories_bp.route('', methods=['POST'])
@admin_required
def create_category():
    """Create a new category (admin only)."""
    data = request.get_json()
    
    nome = data.get('nome', '').strip()
    descrizione = data.get('descrizione', '').strip()
    
    if not nome:
        return jsonify({'error': 'Nome categoria è obbligatorio'}), 400
    
    # Check if exists
    existing = execute_query(
        "SELECT id FROM categorie WHERE nome = %s",
        (nome,),
        fetchone=True
    )
    if existing:
        return jsonify({'error': 'Categoria già esistente'}), 400
    
    category_id = execute_insert(
        "INSERT INTO categorie (nome, descrizione, created_at) VALUES (%s, %s, NOW())",
        (nome, descrizione)
    )
    
    return jsonify({'message': 'Categoria creata', 'category_id': category_id}), 201


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Update a category (admin only)."""
    data = request.get_json()
    
    nome = data.get('nome', '').strip()
    descrizione = data.get('descrizione', '').strip()
    
    if not nome:
        return jsonify({'error': 'Nome categoria è obbligatorio'}), 400
    
    # Check if exists
    category = execute_query(
        "SELECT id FROM categorie WHERE id = %s",
        (category_id,),
        fetchone=True
    )
    if not category:
        return jsonify({'error': 'Categoria non trovata'}), 404
    
    # Check for duplicate name
    existing = execute_query(
        "SELECT id FROM categorie WHERE nome = %s AND id != %s",
        (nome, category_id),
        fetchone=True
    )
    if existing:
        return jsonify({'error': 'Nome categoria già in uso'}), 400
    
    execute_update(
        "UPDATE categorie SET nome = %s, descrizione = %s WHERE id = %s",
        (nome, descrizione, category_id)
    )
    
    return jsonify({'message': 'Categoria aggiornata'})


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """Delete a category (admin only)."""
    # Check if exists
    category = execute_query(
        "SELECT id FROM categorie WHERE id = %s",
        (category_id,),
        fetchone=True
    )
    if not category:
        return jsonify({'error': 'Categoria non trovata'}), 404
    
    # Check if category has posts
    posts = execute_query(
        "SELECT COUNT(*) as count FROM post_categorie WHERE categoria_id = %s",
        (category_id,),
        fetchone=True
    )
    if posts and posts['count'] > 0:
        return jsonify({'error': 'Impossibile eliminare categoria con post associati'}), 400
    
    execute_update("DELETE FROM categorie WHERE id = %s", (category_id,))
    
    return jsonify({'message': 'Categoria eliminata'})


@categories_bp.route('/<int:category_id>/subscribe', methods=['POST'])
@login_required
def subscribe_category(category_id):
    """Subscribe to a category."""
    user = get_current_user()
    
    # Check if exists
    category = execute_query(
        "SELECT id FROM categorie WHERE id = %s",
        (category_id,),
        fetchone=True
    )
    if not category:
        return jsonify({'error': 'Categoria non trovata'}), 404
    
    # Check if already subscribed
    existing = execute_query(
        "SELECT 1 FROM category_subscriptions WHERE user_id = %s AND categoria_id = %s",
        (user['id'], category_id),
        fetchone=True
    )
    if existing:
        return jsonify({'message': 'Già iscritto a questa categoria'})
    
    execute_insert(
        "INSERT INTO category_subscriptions (user_id, categoria_id, created_at) VALUES (%s, %s, NOW())",
        (user['id'], category_id)
    )
    
    return jsonify({'message': 'Iscrizione completata'})


@categories_bp.route('/<int:category_id>/unsubscribe', methods=['POST'])
@login_required
def unsubscribe_category(category_id):
    """Unsubscribe from a category."""
    user = get_current_user()
    
    execute_update(
        "DELETE FROM category_subscriptions WHERE user_id = %s AND categoria_id = %s",
        (user['id'], category_id)
    )
    
    return jsonify({'message': 'Iscrizione annullata'})


@categories_bp.route('/my-subscriptions', methods=['GET'])
@login_required
def get_my_subscriptions():
    """Get current user's subscribed categories."""
    user = get_current_user()
    
    subscriptions = execute_query(
        """SELECT c.id, c.nome, c.descrizione
           FROM categorie c
           JOIN category_subscriptions cs ON cs.categoria_id = c.id
           WHERE cs.user_id = %s
           ORDER BY c.nome""",
        (user['id'],)
    )
    
    return jsonify({'subscriptions': subscriptions or []})
