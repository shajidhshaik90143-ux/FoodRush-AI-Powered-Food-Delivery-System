from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,current_user
from database.database import db
from database.models import User
from functools import wraps
auth_bp=Blueprint('auth',__name__)

def role_required(role):
    def deco(fn):
        @wraps(fn)
        def wrapper(*a,**k):
            if not current_user.is_authenticated: return redirect(url_for('auth.login'))
            if current_user.role!=role: flash('Access denied','danger'); return redirect(url_for('customer.dashboard'))
            return fn(*a,**k)
        return wrapper
    return deco
@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=User.query.filter_by(email=request.form['email'].lower().strip()).first()
        if u and u.check_password(request.form['password']):
            login_user(u)
            return redirect(url_for({'admin':'admin.dashboard','restaurant':'restaurant.dashboard'}.get(u.role,'customer.dashboard')))
        flash('Invalid email or password','danger')
    return render_template('auth/login.html')
@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name', '').strip()
        email=request.form.get('email', '').lower().strip()
        password=request.form.get('password', '')
        if not name:
            flash('Name is required','warning'); return render_template('auth/register.html')
        from utils.validators import valid_email
        if not valid_email(email):
            flash('Please enter a valid email address','warning'); return render_template('auth/register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered','warning'); return render_template('auth/register.html')
        if len(password)<6:
            flash('Password must be at least 6 characters','warning'); return render_template('auth/register.html')
        u=User(name=name,email=email); u.set_password(password); db.session.add(u); db.session.commit()
        flash('Registration successful. Please login.','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
@auth_bp.route('/logout')
def logout(): logout_user(); return redirect(url_for('auth.login'))
