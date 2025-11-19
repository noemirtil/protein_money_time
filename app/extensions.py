from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# Initialize extensions
csrf = CSRFProtect()
login_manager = LoginManager()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'