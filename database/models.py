from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db

def utc_now():
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True); name=db.Column(db.String(100),nullable=False); email=db.Column(db.String(120),unique=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False); role=db.Column(db.String(20),default='customer'); created_at=db.Column(db.DateTime,default=utc_now)
    orders=db.relationship('Order',backref='customer',lazy=True)
    def set_password(self,p): self.password_hash=generate_password_hash(p)
    def check_password(self,p): return check_password_hash(self.password_hash,p)
class Restaurant(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False); description=db.Column(db.Text); cuisine=db.Column(db.String(80)); address=db.Column(db.String(255)); delivery_fee=db.Column(db.Float,default=30); rating=db.Column(db.Float,default=4.0); owner_id=db.Column(db.Integer,db.ForeignKey('user.id')); is_active=db.Column(db.Boolean,default=True)
    foods=db.relationship('Food',backref='restaurant',lazy=True,cascade='all, delete-orphan'); orders=db.relationship('Order',backref='restaurant',lazy=True)
class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(80),unique=True,nullable=False)
    foods=db.relationship('Food',backref='category',lazy=True)
class Food(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False); description=db.Column(db.Text); price=db.Column(db.Float,nullable=False); image=db.Column(db.String(255)); is_veg=db.Column(db.Boolean,default=True); available=db.Column(db.Boolean,default=True); restaurant_id=db.Column(db.Integer,db.ForeignKey('restaurant.id'),nullable=False); category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
class CartItem(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False); food_id=db.Column(db.Integer,db.ForeignKey('food.id'),nullable=False); quantity=db.Column(db.Integer,default=1); food=db.relationship('Food')
    __table_args__=(db.UniqueConstraint('user_id','food_id',name='uq_cart_user_food'),)
class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False); restaurant_id=db.Column(db.Integer,db.ForeignKey('restaurant.id'),nullable=False); status=db.Column(db.String(40),default='Pending'); total=db.Column(db.Float,default=0); address=db.Column(db.String(255)); payment_status=db.Column(db.String(30),default='Pending'); created_at=db.Column(db.DateTime,default=utc_now)
    items=db.relationship('OrderItem',backref='order',lazy=True,cascade='all, delete-orphan')
class OrderItem(db.Model):
    id=db.Column(db.Integer,primary_key=True); order_id=db.Column(db.Integer,db.ForeignKey('order.id'),nullable=False); food_id=db.Column(db.Integer,db.ForeignKey('food.id'),nullable=False); quantity=db.Column(db.Integer,nullable=False); price=db.Column(db.Float,nullable=False); food=db.relationship('Food')
class Review(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); restaurant_id=db.Column(db.Integer,db.ForeignKey('restaurant.id')); food_id=db.Column(db.Integer,db.ForeignKey('food.id')); rating=db.Column(db.Integer,nullable=False); comment=db.Column(db.Text); created_at=db.Column(db.DateTime,default=utc_now)
class Favorite(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); food_id=db.Column(db.Integer,db.ForeignKey('food.id')); food=db.relationship('Food')
class Notification(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); message=db.Column(db.String(255)); is_read=db.Column(db.Boolean,default=False); created_at=db.Column(db.DateTime,default=utc_now)
