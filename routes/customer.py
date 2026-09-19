from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from database.models import Restaurant,Food,Order,Favorite,Review,Category
from database.database import db
from ai.recommender import recommend_for_user
customer_bp=Blueprint('customer',__name__)
@customer_bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'restaurant':
        return redirect(url_for('restaurant.dashboard'))
    return redirect(url_for('customer.dashboard'))

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    foods=Food.query.filter_by(available=True).limit(8).all(); restaurants=Restaurant.query.filter_by(is_active=True).all(); recs=recommend_for_user(current_user.id,6); return render_template('customer/dashboard.html',foods=foods,restaurants=restaurants,recs=recs)
@customer_bp.route('/restaurants')
def restaurants():
    q=request.args.get('q','').strip(); query=Restaurant.query.filter_by(is_active=True)
    if q: query=query.filter(Restaurant.name.ilike(f'%{q}%')|Restaurant.cuisine.ilike(f'%{q}%'))
    return render_template('customer/restaurants.html',restaurants=query.all(),q=q)
@customer_bp.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    r=db.get_or_404(Restaurant, restaurant_id); return render_template('customer/restaurant_detail.html',restaurant=r)
@customer_bp.route('/favorites')
@login_required
def favorites(): return render_template('customer/favorites.html',favorites=Favorite.query.filter_by(user_id=current_user.id).all())
@customer_bp.route('/favorite/<int:food_id>',methods=['POST'])
@login_required
def favorite(food_id):
    f=db.get_or_404(Food, food_id); x=Favorite.query.filter_by(user_id=current_user.id,food_id=f.id).first()
    if x: db.session.delete(x); flash('Removed from favorites','info')
    else: db.session.add(Favorite(user_id=current_user.id,food_id=f.id)); flash('Added to favorites','success')
    db.session.commit(); return redirect(request.referrer or url_for('customer.dashboard'))
@customer_bp.route('/recommendations')
@login_required
def recommendations(): return render_template('customer/recommendations.html',foods=recommend_for_user(current_user.id,20))
@customer_bp.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if request.method=='POST': current_user.name=request.form['name'].strip(); db.session.commit(); flash('Profile updated','success')
    return render_template('customer/profile.html')
@customer_bp.route('/review/<int:restaurant_id>',methods=['POST'])
@login_required
def review(restaurant_id):
    db.get_or_404(Restaurant, restaurant_id)
    try:
        rating=max(1,min(5,int(request.form.get('rating', 5))))
    except (ValueError, TypeError):
        rating=5
    db.session.add(Review(user_id=current_user.id,restaurant_id=restaurant_id,rating=rating,comment=request.form.get('comment','')))
    db.session.commit()
    # Update restaurant average rating
    all_reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
    if all_reviews:
        rest = db.session.get(Restaurant, restaurant_id)
        if rest:
            rest.rating = round(sum(r.rating for r in all_reviews) / len(all_reviews), 1)
            db.session.commit()
    flash('Review added','success')
    return redirect(url_for('customer.restaurant_detail',restaurant_id=restaurant_id))
