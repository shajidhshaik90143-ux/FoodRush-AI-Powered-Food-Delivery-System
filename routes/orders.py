from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from database.database import db
from database.models import CartItem,Order,OrderItem,Restaurant,Notification
orders_bp=Blueprint('orders',__name__)
@orders_bp.route('/checkout',methods=['GET','POST'])
@login_required
def checkout():
    items=CartItem.query.filter_by(user_id=current_user.id).all()
    if not items: flash('Your cart is empty','warning'); return redirect(url_for('cart.cart'))
    restaurants={i.food.restaurant_id for i in items}
    if len(restaurants)!=1: flash('Please order from one restaurant at a time','warning'); return redirect(url_for('cart.cart'))
    r=db.session.get(Restaurant, next(iter(restaurants)))
    if not r: flash('Restaurant not found','danger'); return redirect(url_for('cart.cart'))
    subtotal=sum(i.food.price*i.quantity for i in items); total=subtotal+r.delivery_fee
    if request.method=='POST':
        payment_method = request.form.get('payment', 'cod')
        o=Order(user_id=current_user.id,restaurant_id=r.id,total=total,address=request.form['address'],payment_status='Pending' if payment_method=='cod' else 'Paid')
        db.session.add(o); db.session.flush()
        for i in items: db.session.add(OrderItem(order_id=o.id,food_id=i.food_id,quantity=i.quantity,price=i.food.price)); db.session.delete(i)
        db.session.add(Notification(user_id=current_user.id,message=f'Order #{o.id} placed successfully'))
        db.session.commit(); return redirect(url_for('orders.detail',order_id=o.id))
    return render_template('customer/checkout.html',items=items,restaurant=r,subtotal=subtotal,total=total)
@orders_bp.route('/orders')
@login_required
def history(): return render_template('customer/orders.html',orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all())
@orders_bp.route('/orders/<int:order_id>')
@login_required
def detail(order_id):
    o=db.get_or_404(Order, order_id)
    if current_user.role == 'admin':
        pass
    elif current_user.role == 'restaurant':
        if o.restaurant.owner_id != current_user.id:
            return 'Forbidden', 403
    elif o.user_id != current_user.id:
        return 'Forbidden', 403
    return render_template('customer/order_detail.html',order=o)
