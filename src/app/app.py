from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app

if __name__ == '__main__':
    create_app().run(debug=True)

