from flask import Blueprint, request, jsonify
from database import execute_query, execute_insert, execute_update
from routes.auth import get_current_user, login_required

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    """Get all posts with optional filters."""
    category_id = request.args.get('category')
    status = request.args.get('status')  # OPEN or CLOSED
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page
    
    # Build query
    query = """
        SELECT p.id, p.titolo_post as titolo, p.descrizione, p.data_inserimento, p.status, p.data_chiusura,
               u.id as autore_id, u.nickname as autore_nickname, u.nome as autore_nome,
               (SELECT COUNT(*) FROM commenti c WHERE c.post_id = p.id AND c.deleted_at IS NULL) as commenti_count,
               GROUP_CONCAT(DISTINCT cat.nome ORDER BY cat.nome SEPARATOR ', ') as categorie
        FROM posts p
        JOIN users u ON u.id = p.autore_id
        LEFT JOIN post_categorie pc ON pc.post_id = p.id
        LEFT JOIN categorie cat ON cat.id = pc.categoria_id
        WHERE p.deleted_at IS NULL
    """
    params = []
    
    if category_id:
        query += " AND pc.categoria_id = %s"
        params.append(category_id)
    
    if status:
        query += " AND p.status = %s"
        params.append(status)
    
    if search:
        query += " AND (p.titolo_post LIKE %s OR p.descrizione LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += " GROUP BY p.id ORDER BY p.data_inserimento DESC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])
    
    posts = execute_query(query, params)
    
    # Get total count
    count_query = """
        SELECT COUNT(DISTINCT p.id) as total
        FROM posts p
        LEFT JOIN post_categorie pc ON pc.post_id = p.id
        WHERE p.deleted_at IS NULL
    """
    count_params = []
    
    if category_id:
        count_query += " AND pc.categoria_id = %s"
        count_params.append(category_id)
    
    if status:
        count_query += " AND p.status = %s"
        count_params.append(status)
    
    if search:
        count_query += " AND (p.titolo_post LIKE %s OR p.descrizione LIKE %s)"
        count_params.extend([f'%{search}%', f'%{search}%'])
    
    total = execute_query(count_query, count_params, fetchone=True)
    
    return jsonify({
        'posts': posts or [],
        'total': total['total'] if total else 0,
        'page': page,
        'per_page': per_page
    })


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get single post with details."""
    post = execute_query(
        """SELECT p.id, p.titolo_post as titolo, p.descrizione, p.data_inserimento, p.status, 
                  p.data_chiusura, p.solution_comment_id, p.final_solution_text,
                  u.id as autore_id, u.nickname as autore_nickname, u.nome as autore_nome
           FROM posts p
           JOIN users u ON u.id = p.autore_id
           WHERE p.id = %s AND p.deleted_at IS NULL""",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    # Get categories
    categories = execute_query(
        """SELECT c.id, c.nome
           FROM categorie c
           JOIN post_categorie pc ON pc.categoria_id = c.id
           WHERE pc.post_id = %s""",
        (post_id,)
    )
    
    # Get media
    media = execute_query(
        "SELECT id, tipo, url FROM post_media WHERE post_id = %s",
        (post_id,)
    )
    
    # Check if author is expert in any of the post's categories
    is_expert = execute_query(
        """SELECT 1 FROM user_category_stats ucs
           JOIN post_categorie pc ON pc.categoria_id = ucs.categoria_id
           WHERE ucs.user_id = %s AND pc.post_id = %s AND ucs.is_expert = 1
           LIMIT 1""",
        (post['autore_id'], post_id),
        fetchone=True
    )
    
    post['categorie'] = categories or []
    post['media'] = media or []
    post['autore_is_expert'] = bool(is_expert)
    
    return jsonify({'post': post})


@posts_bp.route('', methods=['POST'])
@login_required
def create_post():
    """Create a new post."""
    user = get_current_user()
    data = request.get_json()
    
    titolo = data.get('titolo', '').strip()
    descrizione = data.get('descrizione', '').strip()
    categorie = data.get('categorie', [])  # List of category IDs
    media_urls = data.get('media', [])  # List of {tipo: 'IMAGE'|'VIDEO', url: '...'}
    
    # Validation
    if not titolo:
        return jsonify({'error': 'Titolo è obbligatorio'}), 400
    
    if not descrizione:
        return jsonify({'error': 'Descrizione è obbligatoria'}), 400
    
    if not categorie or len(categorie) == 0:
        return jsonify({'error': 'Seleziona almeno una categoria'}), 400
    
    # Create post
    post_id = execute_insert(
        """INSERT INTO posts (titolo_post, descrizione, autore_id, data_inserimento, status)
           VALUES (%s, %s, %s, NOW(), 'OPEN')""",
        (titolo, descrizione, user['id'])
    )
    
    # Add categories
    for cat_id in categorie:
        execute_insert(
            "INSERT INTO post_categorie (post_id, categoria_id) VALUES (%s, %s)",
            (post_id, cat_id)
        )
    
    # Add media
    for m in media_urls:
        execute_insert(
            "INSERT INTO post_media (post_id, tipo, url, created_at) VALUES (%s, %s, %s, NOW())",
            (post_id, m.get('tipo', 'IMAGE'), m.get('url'))
        )
    
    # Create notifications for subscribed users
    subscribed_users = execute_query(
        """SELECT DISTINCT cs.user_id
           FROM category_subscriptions cs
           WHERE cs.categoria_id IN ({}) AND cs.user_id != %s""".format(
               ','.join(['%s'] * len(categorie))
           ),
        tuple(categorie) + (user['id'],)
    )
    
    for sub in (subscribed_users or []):
        execute_insert(
            """INSERT INTO notifications (user_id, tipo, messaggio, post_id, created_at)
               VALUES (%s, 'NEW_POST_IN_CATEGORY', %s, %s, NOW())""",
            (sub['user_id'], f"Nuovo post: {titolo}", post_id)
        )
    
    return jsonify({'message': 'Post creato', 'post_id': post_id}), 201


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    """Update a post."""
    user = get_current_user()
    
    # Check ownership
    post = execute_query(
        "SELECT autore_id, status FROM posts WHERE id = %s AND deleted_at IS NULL",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    if post['autore_id'] != user['id'] and user['role'] != 'ADMIN':
        return jsonify({'error': 'Non autorizzato'}), 403
    
    data = request.get_json()
    titolo = data.get('titolo', '').strip()
    descrizione = data.get('descrizione', '').strip()
    
    if not titolo or not descrizione:
        return jsonify({'error': 'Titolo e descrizione sono obbligatori'}), 400
    
    execute_update(
        "UPDATE posts SET titolo_post = %s, descrizione = %s WHERE id = %s",
        (titolo, descrizione, post_id)
    )
    
    return jsonify({'message': 'Post aggiornato'})


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    """Soft delete a post."""
    user = get_current_user()
    
    # Check ownership
    post = execute_query(
        "SELECT autore_id FROM posts WHERE id = %s AND deleted_at IS NULL",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    if post['autore_id'] != user['id'] and user['role'] != 'ADMIN':
        return jsonify({'error': 'Non autorizzato'}), 403
    
    # Soft delete post and its comments
    execute_update("UPDATE posts SET deleted_at = NOW() WHERE id = %s", (post_id,))
    execute_update("UPDATE commenti SET deleted_at = NOW() WHERE post_id = %s", (post_id,))
    
    return jsonify({'message': 'Post eliminato'})


@posts_bp.route('/<int:post_id>/close', methods=['POST'])
@login_required
def close_post(post_id):
    """Close a post with a solution."""
    user = get_current_user()
    
    # Check ownership
    post = execute_query(
        "SELECT autore_id, status FROM posts WHERE id = %s AND deleted_at IS NULL",
        (post_id,),
        fetchone=True
    )
    
    if not post:
        return jsonify({'error': 'Post non trovato'}), 404
    
    if post['autore_id'] != user['id']:
        return jsonify({'error': 'Solo l\'autore può chiudere il post'}), 403
    
    if post['status'] == 'CLOSED':
        return jsonify({'error': 'Post già chiuso'}), 400
    
    data = request.get_json()
    solution_comment_id = data.get('solution_comment_id')
    final_solution_text = data.get('final_solution_text', '').strip()
    
    if not solution_comment_id and not final_solution_text:
        return jsonify({'error': 'Specifica un commento risolutivo o una soluzione finale'}), 400
    
    if solution_comment_id:
        # Verify comment exists and belongs to this post
        comment = execute_query(
            "SELECT id FROM commenti WHERE id = %s AND post_id = %s AND deleted_at IS NULL",
            (solution_comment_id, post_id),
            fetchone=True
        )
        if not comment:
            return jsonify({'error': 'Commento non trovato'}), 404
        
        execute_update(
            """UPDATE posts SET status = 'CLOSED', data_chiusura = NOW(), 
                      solution_comment_id = %s, final_solution_text = NULL 
               WHERE id = %s""",
            (solution_comment_id, post_id)
        )
    else:
        execute_update(
            """UPDATE posts SET status = 'CLOSED', data_chiusura = NOW(), 
                      solution_comment_id = NULL, final_solution_text = %s 
               WHERE id = %s""",
            (final_solution_text, post_id)
        )
    
    return jsonify({'message': 'Post chiuso con successo'})


@posts_bp.route('/my', methods=['GET'])
@login_required
def get_my_posts():
    """Get posts by current user."""
    user = get_current_user()
    
    posts = execute_query(
        """SELECT p.id, p.titolo_post as titolo, p.descrizione, p.data_inserimento, p.status, p.data_chiusura,
                  (SELECT COUNT(*) FROM commenti c WHERE c.post_id = p.id AND c.deleted_at IS NULL) as commenti_count,
                  GROUP_CONCAT(DISTINCT cat.nome ORDER BY cat.nome SEPARATOR ', ') as categorie
           FROM posts p
           LEFT JOIN post_categorie pc ON pc.post_id = p.id
           LEFT JOIN categorie cat ON cat.id = pc.categoria_id
           WHERE p.autore_id = %s AND p.deleted_at IS NULL
           GROUP BY p.id
           ORDER BY p.data_inserimento DESC""",
        (user['id'],)
    )
    
    return jsonify({'posts': posts or []})
