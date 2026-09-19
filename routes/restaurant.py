from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from database.database import db
from database.models import Restaurant,Food,Order,Category
from routes.auth import role_required
restaurant_bp=Blueprint('restaurant',__name__,url_prefix='/restaurant')
def my_restaurant():
    r = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not r:
        r = Restaurant(name=f"{current_user.name}'s Kitchen", description='Delicious freshly cooked meals', cuisine='Multi-Cuisine', address='Main Street', owner_id=current_user.id, delivery_fee=30.0, rating=4.5)
        db.session.add(r)
        db.session.commit()
    return r

@restaurant_bp.route('/dashboard')
@login_required
@role_required('restaurant')
def dashboard():
    r=my_restaurant(); return render_template('restaurant/dashboard.html',restaurant=r,orders=Order.query.filter_by(restaurant_id=r.id).order_by(Order.created_at.desc()).limit(10).all())
@restaurant_bp.route('/menu')
@login_required
@role_required('restaurant')
def menu(): return render_template('restaurant/menu.html',restaurant=my_restaurant())
@restaurant_bp.route('/food/add',methods=['GET','POST'])
@login_required
@role_required('restaurant')
def add_food():
    r=my_restaurant()
    if request.method=='POST':
        name = request.form.get('name', '').strip()
        cat_name = request.form.get('category', '').strip()
        try:
            price = float(request.form.get('price', 0))
            if price < 0:
                raise ValueError()
        except (ValueError, TypeError):
            flash('Please enter a valid positive price', 'warning')
            return render_template('restaurant/add_food.html')
        if not name or not cat_name:
            flash('Food name and category are required', 'warning')
            return render_template('restaurant/add_food.html')
        c=Category.query.filter_by(name=cat_name).first()
        if not c: c=Category(name=cat_name); db.session.add(c); db.session.flush()
        db.session.add(Food(name=name,description=request.form.get('description',''),price=price,restaurant_id=r.id,category_id=c.id,is_veg='is_veg' in request.form))
        db.session.commit()
        flash(f'{name} added to menu', 'success')
        return redirect(url_for('restaurant.menu'))
    return render_template('restaurant/add_food.html')
@restaurant_bp.route('/food/<int:food_id>/delete',methods=['POST'])
@login_required
@role_required('restaurant')
def delete_food(food_id):
    r=my_restaurant()
    f=Food.query.filter_by(id=food_id,restaurant_id=r.id).first_or_404()
    try:
        db.session.delete(f)
        db.session.commit()
        flash(f'{f.name} deleted successfully', 'success')
    except Exception:
        db.session.rollback()
        f.available = False
        db.session.commit()
        flash(f'{f.name} has past order history, so it was marked as unavailable instead.', 'info')
    return redirect(url_for('restaurant.menu'))
@restaurant_bp.route('/orders')
@login_required
@role_required('restaurant')
def orders(): return render_template('restaurant/orders.html',orders=Order.query.filter_by(restaurant_id=my_restaurant().id).order_by(Order.created_at.desc()).all())
@restaurant_bp.route('/order/<int:order_id>/status',methods=['POST'])
@login_required
@role_required('restaurant')
def update_status(order_id):
    r=my_restaurant()
    o=Order.query.filter_by(id=order_id,restaurant_id=r.id).first_or_404()
    new_status = request.form.get('status', o.status)
    o.status = new_status
    db.session.commit()
    from services.notification_service import notify
    notify(o.user_id, f'Your order #{o.id} status changed to {new_status}')
    flash(f'Order #{o.id} status updated to {new_status}', 'success')
    return redirect(url_for('restaurant.orders'))
