from flask import Flask
from dotenv import load_dotenv
from .db.connection import get_db
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-key"),
        WTF_CSRF_ENABLED=True,
    )

    # Initialize extensions
    from .extensions import csrf, login_manager

    csrf.init_app(app)
    login_manager.init_app(app)

    # --- Register Database Teardown ---
    from .db import connection

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
    from app.routes.presave import presave_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(presave_bp)

    app.add_url_rule("/", endpoint="index")

    return app
