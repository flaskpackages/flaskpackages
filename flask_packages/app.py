import os

from flask import Flask

db_password = os.environ['DBPASSWD']
db_connection = os.environ['DBCONN']
db_name = 'flask_db'
password_salt = os.environ['PASSWDSALT']
secret_key = os.environ['SECR_KEY']

def create_app(template_folder):
    # Create app
    app = Flask(__name__, template_folder=template_folder)
    app.config['DEBUG'] = True
    app.config['SECURITY_PASSWORD_SALT'] = password_salt
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['MONGODB_HOST'] = {'mongodb+srv://user:'+db_password+'@'+db_connection+'/'+db_name+'?retryWrites=true&w=majority'}
    app.config['SECRET_KEY'] = secret_key
    return app