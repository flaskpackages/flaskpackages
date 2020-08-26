import os

from flask import Flask
from flask_caching import Cache

flask_packages_enviro = os.environ['FLASK_PACKAGES_ENVIRO']
split = flask_packages_enviro.split(',')
db_password = split[0]
db_connection = split[1]
db_name = split[2]
password_salt = split[3]
secret_key = split[4]

def create_app(template_folder):
    # Create app
    app = Flask(__name__, template_folder=template_folder)
    app.config['DEBUG'] = True
    app.config['SECURITY_PASSWORD_SALT'] = password_salt
    app.config['SECRET_KEY'] = secret_key
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

    #app.config['MONGODB_HOST'] = {'mongomock://localhost'}
    app.config['MONGODB_HOST'] = {'mongodb+srv://user:'+db_password+'@'+db_connection+'/'+db_name+'?retryWrites=true&w=majority'}
    return app
