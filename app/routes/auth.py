from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/test')
def test():
    return '<h2>Auth blueprint is working! ✅</h2>'