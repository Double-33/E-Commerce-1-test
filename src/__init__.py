from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config.from_pyfile('config.py')

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    from .routes import api
    app.register_blueprint(api)

    return app
