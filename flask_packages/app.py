import os

from flask import Flask


def create_app(template_folder):
    # Create app
    app = Flask(__name__, template_folder=template_folder)
    app.config["DEBUG"] = os.environ.get("DEBUG", False)
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("PASSWORD_SALT", "default_salt")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "test")
    app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"
    app.config["MONGODB_DB"] = 'flask_db'
    app.config["MONGODB_HOST"] = {os.environ.get("MONGODB_CONNECTION_STRING", 'mongomock://localhost')}
    app.config["SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS"] = True
    return app
