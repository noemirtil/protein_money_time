from flask import Flask
from config import Config
from app.extensions import csrf, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Initialize extensions
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # Inicia base de datos con comands CLI
    #flask init-db
    from app.db import connection
    connection.init_app(app)
    
    #Register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Test route
    @app.route('/')
    def index():
        return '<h1>Protein Money Time App is Running! 🍽️</h1>'
    
    return app