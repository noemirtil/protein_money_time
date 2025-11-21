from flask import Blueprint, render_template, url_for, redirect, flash
from app.db.connection import get_db
from config import Config
from psycopg2.extras import RealDictCursor
from app.forms.auth_forms import RegistrationForm
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@auth_bp.route('/test')
def test():
    return '<h2>Auth blueprint is working! ✅</h2>'
    
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    db = get_db()
    cur = db.cursor()
    if form.validate_on_submit():
        try:
            username = form.username.data.strip().lower()
            email = form.email.data.strip().lower()
            hashed_password = generate_password_hash(form.password.data)
            
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            
            db.commit()
            
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.rollback()
            print(f"❌ ERROR: {e}")  # ← Add this to see the actual error!
            print(f"Error type: {type(e)}")
            
            if 'unique' in str(e).lower():
                flash('Este usuario o email ya existe.', 'error')
            else:
                flash('Error al registrar. Intenta de nuevo.', 'error')
            
    return render_template('auth/register.html', form=form)
            
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')
            