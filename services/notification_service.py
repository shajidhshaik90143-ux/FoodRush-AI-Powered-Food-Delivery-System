from database.database import db
from database.models import Notification
def notify(user_id,message): db.session.add(Notification(user_id=user_id,message=message)); db.session.commit()
