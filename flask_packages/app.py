import os

from flask import Flask


def create_app(template_folder):
    # Create app
    app = Flask(__name__, template_folder=template_folder)
    app.config['DEBUG'] = True

    # Generate a nice key using secrets.token_urlsafe()
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'TEST')
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", 'TEST')

    # MongoDB Config
    app.config['MONGODB_DB'] = 'flackpackages'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017

    return app
