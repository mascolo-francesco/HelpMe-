from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from config import Config
import database


def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(config_class)
    
    # Enable CORS for API
    CORS(app, supports_credentials=True)
    
    # Initialize database
    database.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.posts import posts_bp
    from routes.comments import comments_bp
    from routes.categories import categories_bp
    from routes.votes import votes_bp
    from routes.notifications import notifications_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(posts_bp, url_prefix='/api/v1/posts')
    app.register_blueprint(comments_bp, url_prefix='/api/v1/comments')
    app.register_blueprint(categories_bp, url_prefix='/api/v1/categories')
    app.register_blueprint(votes_bp, url_prefix='/api/v1/votes')
    app.register_blueprint(notifications_bp, url_prefix='/api/v1/notifications')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    
    # Serve SPA frontend
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        # Try to serve the file, fall back to index.html for SPA routing
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    return app


if __name__ == '__main__':
    import os
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
