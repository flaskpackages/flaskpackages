import os

from flask import render_template, send_from_directory
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    auth_required
)
from flask_security.utils import (hash_password)
from flask_packages.web import app, db
from flask_packages.models import user_datastore, Project

from flask_mongoengine import MongoEngine
import mongoengine as me

# Create a user to test with
@app.before_first_request
def create_user():
    #user_datastore.create_user(
    #        email="admin@admin.com",
    #        password=hash_password("admin"))
    return

# Views
@app.route("/")
def home():
    categories = []
    for package in Project.objects:
        classifier = package.classifiers
        topics = classifier['Topic']
        for topic in topics:
            topic = topic.split("::")
            categories.append(topic[0].strip())
        import pdb; pdb.set_trace()
    return render_template('index.html', principal_categories=categories)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
