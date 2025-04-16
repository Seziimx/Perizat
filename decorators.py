from functools import wraps
from flask import session, redirect, url_for, flash

def login_required_with_role(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role')
            if not session.get('user_id'):
                flash("Пожалуйста, войдите в систему", "warning")
                return redirect(url_for('auth_bp.login'))
            if role and user_role != role:
                flash("Недостаточно прав доступа", "danger")
                return redirect(url_for('dashboard_bp.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
