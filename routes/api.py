from flask import Blueprint,jsonify,request
from database.models import Food,Restaurant
api_bp=Blueprint('api',__name__)
@api_bp.get('/foods')
def foods():
    q=request.args.get('q',''); fs=Food.query.filter(Food.available.is_(True),Food.name.ilike(f'%{q}%')).all(); return jsonify([{'id':f.id,'name':f.name,'price':f.price,'restaurant':f.restaurant.name,'veg':f.is_veg} for f in fs])
@api_bp.get('/restaurants')
def restaurants(): return jsonify([{'id':r.id,'name':r.name,'cuisine':r.cuisine,'rating':r.rating} for r in Restaurant.query.filter_by(is_active=True).all()])
