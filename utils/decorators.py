from functools import wraps
from flask import redirect,url_for,flash
from flask_login import current_user
def role_required(role):
    def deco(fn):
        @wraps(fn)
        def wrapper(*a,**k):
            if not current_user.is_authenticated: return redirect(url_for('auth.login'))
            if current_user.role!=role: flash('Access denied','danger'); return redirect(url_for('customer.dashboard'))
            return fn(*a,**k)
        return wrapper
    return deco
