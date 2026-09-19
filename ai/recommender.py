from database.models import Food,Order,OrderItem,Review
from database.database import db

def recommend_for_user(user_id,limit=6):
    ordered_ids=[x.food_id for o in Order.query.filter_by(user_id=user_id).all() for x in o.items]
    if not ordered_ids: return Food.query.filter_by(available=True).order_by(Food.id.desc()).limit(limit).all()
    ordered=Food.query.filter(Food.id.in_(ordered_ids)).all(); cats={f.category_id for f in ordered if f.category_id}
    q=Food.query.filter(Food.available.is_(True),Food.id.notin_(ordered_ids))
    if cats: q=q.filter(Food.category_id.in_(cats))
    return q.limit(limit).all()
