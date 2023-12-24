import sys
print(sys.path)

import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import db, User, Product, Order, OrderProduct
from app.routes import api, UserResource, ProductResource, CartResource

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    JWT_SECRET_KEY = 'test_jwt_secret_key'

class TestAPI(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object(TestConfig)
        app.config['JWT_TOKEN_LOCATION'] = ['headers']
        app.config['JWT_HEADER_NAME'] = 'Authorization'
        app.config['JWT_HEADER_TYPE'] = 'Bearer'

        with app.app_context():
            db.init_app(app)
            db.create_all()

        app.register_blueprint(api)

        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ... rest of your test code
