from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from database.database import db
from database.models import User,Restaurant,Food,Order
from routes.auth import role_required
admin_bp=Blueprint('admin',__name__,url_prefix='/admin')
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard(): return render_template('admin/dashboard.html',users=User.query.count(),restaurants=Restaurant.query.count(),foods=Food.query.count(),orders=Order.query.count(),revenue=sum(o.total for o in Order.query.all()),recent=Order.query.order_by(Order.created_at.desc()).limit(10).all())
@admin_bp.route('/users')
@login_required
@role_required('admin')
def users(): return render_template('admin/users.html',users=User.query.order_by(User.created_at.desc()).all())
@admin_bp.route('/restaurants')
@login_required
@role_required('admin')
def restaurants(): return render_template('admin/restaurants.html',restaurants=Restaurant.query.all())
@admin_bp.route('/restaurants/<int:id>/toggle',methods=['POST'])
@login_required
@role_required('admin')
def toggle_restaurant(id): r=db.get_or_404(Restaurant, id); r.is_active=not r.is_active; db.session.commit(); return redirect(url_for('admin.restaurants'))
@admin_bp.route('/orders')
@login_required
@role_required('admin')
def orders(): return render_template('admin/orders.html',orders=Order.query.order_by(Order.created_at.desc()).all())
