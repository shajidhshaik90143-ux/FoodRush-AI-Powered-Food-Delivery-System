from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from database.database import db
from database.models import Food,CartItem
cart_bp=Blueprint('cart',__name__)
def cart_total(): return sum(x.food.price*x.quantity for x in CartItem.query.filter_by(user_id=current_user.id).all())
@cart_bp.route('/cart')
@login_required
def cart(): return render_template('customer/cart.html',items=CartItem.query.filter_by(user_id=current_user.id).all(),total=cart_total())
@cart_bp.route('/cart/add/<int:food_id>',methods=['POST'])
@login_required
def add(food_id):
    f=db.get_or_404(Food, food_id)
    try:
        q=max(1,int(request.form.get('quantity',1)))
    except (ValueError, TypeError):
        q=1
    x=CartItem.query.filter_by(user_id=current_user.id,food_id=f.id).first()
    if x: x.quantity+=q
    else: db.session.add(CartItem(user_id=current_user.id,food_id=f.id,quantity=q))
    db.session.commit(); flash(f'{f.name} added to cart','success'); return redirect(request.referrer or url_for('cart.cart'))
@cart_bp.route('/cart/update/<int:item_id>',methods=['POST'])
@login_required
def update(item_id):
    x=CartItem.query.filter_by(id=item_id,user_id=current_user.id).first_or_404()
    try:
        q=int(request.form.get('quantity', 1))
    except (ValueError, TypeError):
        q=1
    if q<=0: db.session.delete(x)
    else: x.quantity=q
    db.session.commit(); return redirect(url_for('cart.cart'))
@cart_bp.route('/cart/remove/<int:item_id>',methods=['POST'])
@login_required
def remove(item_id):
    x=CartItem.query.filter_by(id=item_id,user_id=current_user.id).first_or_404(); db.session.delete(x); db.session.commit(); return redirect(url_for('cart.cart'))
