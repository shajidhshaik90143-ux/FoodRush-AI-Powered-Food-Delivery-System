from flask import Flask, render_template
from config import Config
from database.database import db
from flask_login import LoginManager
from database.models import User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    from routes.auth import auth_bp
    from routes.customer import customer_bp
    from routes.restaurant import restaurant_bp
    from routes.admin import admin_bp
    from routes.orders import orders_bp
    from routes.cart import cart_bp
    from routes.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.errorhandler(404)
    def not_found(e): return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def server_error(e): return render_template('errors/500.html'), 500

    from utils.helpers import money
    app.jinja_env.filters['money'] = money

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
