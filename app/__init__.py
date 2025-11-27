from flask import Flask
from config import Config
from app.extensions import csrf, login_manager
from .db.connection import get_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.db import connection

    connection.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        cur = get_db().cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user_dict = cur.fetchone()
        if user_dict:
            return User(user_dict)
        return None

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.product_insert import product_insert_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(product_insert_bp)

    return app
