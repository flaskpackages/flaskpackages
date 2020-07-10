from flask import render_template
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    auth_required,
    hash_password
)
from flask_packages.web import app
from flask_packages.models import user_datastore


# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(
            email="admin@me.com",
            password=hash_password("password"))


# Views
@app.route("/")
@auth_required()
def home():
    return render_template('index.html')
