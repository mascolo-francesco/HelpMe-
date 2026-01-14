from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import execute_query, execute_insert

auth_bp = Blueprint('auth', __name__)


def get_current_user():
    """Get current logged-in user from session."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    user = execute_query(
        "SELECT id, nickname, nome, email, role, status FROM users WHERE id = %s",
        (user_id,),
        fetchone=True
    )
    return user


def login_required(f):
    """Decorator to require login."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return jsonify({'error': 'Login richiesto'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Login richiesto'}), 401
        if user['role'] != 'ADMIN':
            return jsonify({'error': 'Permessi insufficienti'}), 403
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    nickname = data.get('nickname', '').strip()
    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    # Validation
    if not nickname or not nome or not email or not password:
        return jsonify({'error': 'Tutti i campi sono obbligatori'}), 400
    
    if len(nickname) < 3:
        return jsonify({'error': 'Nickname deve avere almeno 3 caratteri'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password deve avere almeno 6 caratteri'}), 400
    
    # Check if nickname or email already exists
    existing = execute_query(
        "SELECT id FROM users WHERE nickname = %s OR email = %s",
        (nickname, email),
        fetchone=True
    )
    if existing:
        return jsonify({'error': 'Nickname o email già in uso'}), 400
    
    # Create user
    password_hash = generate_password_hash(password)
    user_id = execute_insert(
        """INSERT INTO users (nickname, nome, email, password_hash, role, status, created_at) 
           VALUES (%s, %s, %s, %s, 'USER', 'ACTIVE', NOW())""",
        (nickname, nome, email, password_hash)
    )
    
    # Auto login after registration
    session['user_id'] = user_id
    session.permanent = True
    
    return jsonify({
        'message': 'Registrazione completata',
        'user': {
            'id': user_id,
            'nickname': nickname,
            'nome': nome,
            'email': email,
            'role': 'USER'
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    data = request.get_json()
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email e password sono obbligatori'}), 400
    
    user = execute_query(
        """SELECT id, nickname, nome, email, password_hash, role, status 
           FROM users WHERE email = %s""",
        (email,),
        fetchone=True
    )
    
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Credenziali non valide'}), 401
    
    if user['status'] == 'BANNED':
        return jsonify({'error': 'Account sospeso. Contatta un amministratore.'}), 403
    
    session['user_id'] = user['id']
    session.permanent = True
    
    return jsonify({
        'message': 'Login effettuato',
        'user': {
            'id': user['id'],
            'nickname': user['nickname'],
            'nome': user['nome'],
            'email': user['email'],
            'role': user['role']
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user."""
    session.clear()
    return jsonify({'message': 'Logout effettuato'})


@auth_bp.route('/session', methods=['GET'])
def get_session():
    """Get current session info."""
    user = get_current_user()
    if not user:
        return jsonify({'authenticated': False})
    
    return jsonify({
        'authenticated': True,
        'user': {
            'id': user['id'],
            'nickname': user['nickname'],
            'nome': user['nome'],
            'email': user['email'],
            'role': user['role']
        }
    })
