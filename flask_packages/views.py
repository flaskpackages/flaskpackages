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
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# Create a user to test with
@app.before_first_request
def create_user():
    # user_datastore.create_user(
    #        email="admin@admin.com",
    #        password=hash_password("admin"))
    return


# Views
@app.route("/")
@cache.cached(timeout=50)
def home():
    categories = set()
    latest_projects = Project.objects.order_by('-released').limit(5)
    for package in Project.objects:
        classifier = package.classifiers
        if 'topic' in classifier and classifier['topic']:
            topic = classifier['topic']
            topic = topic.split("::")
            categories.add(topic[0].strip())

    return render_template('index.html', principal_categories=categories, latest_projects=latest_projects)


@app.route('/project/<package_name>')
def package(package_name):
    package = Project.objects.get(name=package_name)
    maintainer = package['maintainer']
    maintainer_packages = Project.objects(maintainer=maintainer)

    return render_template('package.html', package=package, maintainer_packages=maintainer_packages)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')