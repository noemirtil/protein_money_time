from flask import Blueprint, render_template, url_for, redirect, flash
from app.db.connection import get_db
from config import Config
from psycopg2.extras import RealDictCursor
from app.forms.auth_forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash
from app.models.user import User
from flask_login import login_user, logout_user, login_required

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
            print(f"❌ ERROR: {e}")
            print(f"Error type: {type(e)}")
            
            if 'unique' in str(e).lower():
                flash('Este usuario o email ya existe.', 'error')
            else:
                flash('Error al registrar. Intenta de nuevo.', 'error')
            
    return render_template('auth/register.html', form=form)
            
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db = get_db()
    cur = db.cursor()
    
    if form.validate_on_submit():
        username_email = form.username_email.data.strip().lower()
        password = form.password.data
        
        try:
            cur.execute(
                'SELECT * FROM users WHERE (username=%s or email=%s)',
                (username_email, username_email,))
            user_dict = cur.fetchone()            
            if user_dict:
                user_obj = User(user_dict)
                if user_obj.is_password_correct(password):
                    login_user(user_obj)
                    flash(f'¡Bienvenid@, {user_obj.username}!', 'success')
                    return redirect(url_for('main.dashboard'))
                else:
                    flash('Credenciales incorrectas. Intente nuevamente.', 'error')
                    return redirect(url_for('auth.login'))
            else:
                flash('Credenciales incorrectas. Intente nuevamente.', 'error')
                return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"❌ ERROR: {e}")
            print(f"Error type: {type(e)}")
            
            flash('Error al ingresar. Intenta de nuevo.', 'error')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada con éxito.', 'success')
    return redirect(url_for('main.index'))
    