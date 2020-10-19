import os

from flask import Flask
from flask_caching import Cache


def create_app(template_folder):
    # Create app
    app = Flask(__name__, template_folder=template_folder)
    app.config['DEBUG'] = True
    app.config['SECURITY_PASSWORD_SALT'] = os.environ['PASSWORD_SALT']
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

    #app.config['MONGODB_HOST'] = {'mongomock://localhost'}
    app.config['MONGODB_HOST'] = {os.environ['MONGODB_CONNECTION_STRING']}
    return app
