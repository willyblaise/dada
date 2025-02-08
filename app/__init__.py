from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# Initialize global objects
db = SQLAlchemy()
bcrypt = Bcrypt()  # Initialize without app
login_manager = LoginManager()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Move import inside function
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    #bcrypt = Bcrypt(app)

    # Initialize the app with extensions
    db.init_app(app)
    migrate = Migrate()
    login_manager.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    from app.routes import app_routes
    #app.register_blueprint(app_routes)
    app.register_blueprint(app_routes, url_prefix='/')


    return app


def register_blueprints(app):
    import app.routes
