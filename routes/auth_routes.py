from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import db, User

auth_bp = Blueprint('auth_bp', __name__)

# Mock user database
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'mechanic': {'password': 'mech123', 'role': 'mechanic'},
    'operator': {'password': 'oper123', 'role': 'operator'},
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Осы бетке кіру үшін жүйеге кіріңіз.', 'danger')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Осы бетке кіру үшін жүйеге кіріңіз.', 'danger')
                return redirect(url_for('auth_bp.login'))
            if session.get('role') not in allowed_roles:
                flash('Қол жеткізу құқығы жеткіліксіз.', 'danger')
                return redirect(url_for('dashboard_bp.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '').strip()

        # Debugging: Print submitted login and password
        print(f"Логин: {login}, Пароль: {password}")

        # Validate input
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role  # Store the user's role in the session
            flash('Сіз жүйеге сәтті кірдіңіз!', 'success')
            return redirect(url_for('dashboard_bp.dashboard'))
        else:
            flash('Логин немесе пароль дұрыс емес!', 'danger')  # Display error message
            return redirect(url_for('auth_bp.login'))  # Redirect back to login page
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Сіз жүйеден шықтыңыз!', 'success')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()

        # Debugging: Print submitted registration data
        print(f"Name: {name}, Login: {login}, Role: {role}")

        # Validate input
        if not name or not login or not password or not role:
            flash('Барлық өрістерді толтыру қажет!', 'danger')
            return redirect(url_for('auth_bp.register'))

        # Check if the user already exists
        if User.query.filter_by(login=login).first():
            flash('Мұндай логині бар пайдаланушы қазірдің өзінде бар!', 'danger')
            return redirect(url_for('auth_bp.register'))

        # Save the new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, login=login, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Set session
        session['user_id'] = new_user.id
        session['role'] = new_user.role
        flash('Тіркеу сәтті өтті!', 'success')
        return redirect(url_for('dashboard_bp.dashboard'))

    return render_template('register.html')
