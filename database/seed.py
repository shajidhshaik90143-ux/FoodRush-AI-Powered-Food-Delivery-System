from app import app
from database.database import db
from database.models import User,Restaurant,Category,Food

def seed():
    if User.query.filter_by(email='admin@foodrush.com').first(): print('Already seeded'); return
    admin=User(name='Admin',email='admin@foodrush.com',role='admin'); admin.set_password('Admin@123'); db.session.add(admin)
    owner=User(name='Demo Restaurant',email='restaurant@foodrush.com',role='restaurant'); owner.set_password('Restaurant@123'); db.session.add(owner); db.session.flush()
    r=Restaurant(name='Spice Hub',description='Indian favorites and fast food',cuisine='Indian',address='Ongole, Andhra Pradesh',owner_id=owner.id,delivery_fee=30,rating=4.4); db.session.add(r)
    cats={}
    for n in ['Pizza','Biryani','Burger','Drinks']:
        c=Category(name=n); db.session.add(c); cats[n]=c
    db.session.flush()
    foods=[('Chicken Biryani','Aromatic dum biryani',220,'Biryani',False),('Veg Biryani','Fragrant vegetable biryani',160,'Biryani',True),('Cheese Pizza','Cheesy classic pizza',199,'Pizza',True),('Chicken Burger','Crispy chicken burger',149,'Burger',False),('Fresh Lime','Chilled lime drink',60,'Drinks',True)]
    for n,d,p,c,v in foods: db.session.add(Food(name=n,description=d,price=p,restaurant_id=r.id,category_id=cats[c].id,is_veg=v))
    db.session.commit(); print('Seed complete')
if __name__=='__main__':
    with app.app_context(): seed()
