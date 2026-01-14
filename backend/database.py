import pymysql
from flask import g, current_app
from werkzeug.local import LocalProxy


def get_db():
    """Get database connection from application context."""
    if 'db' not in g:
        ssl_config = None
        if current_app.config.get('DB_SSL'):
            ssl_config = {'ssl': {'ca': None}}  # Use system CA
        
        g.db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            ssl=ssl_config
        )
    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    """Initialize database with Flask app."""
    app.teardown_appcontext(close_db)


db = LocalProxy(get_db)


def execute_query(query, params=None, fetchone=False, fetchall=True):
    """Execute a query and return results."""
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return cursor.lastrowid


def execute_insert(query, params=None):
    """Execute an insert and return the last inserted ID."""
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.lastrowid


def execute_update(query, params=None):
    """Execute an update/delete and return affected rows."""
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.rowcount
