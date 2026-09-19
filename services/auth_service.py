from database.models import User
def authenticate(email,password):
    u=User.query.filter_by(email=email.lower().strip()).first(); return u if u and u.check_password(password) else None
