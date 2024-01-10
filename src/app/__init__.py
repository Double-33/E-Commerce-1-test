# src/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from src.app.routes import api
    app.register_blueprint(api)

    # Configure Flask-Login
    from src.app.models import User
    login_manager.login_view = 'api.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
