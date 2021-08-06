import os

from flask import render_template, send_from_directory
from flask_caching import Cache

from flask_packages.models import Project
from flask_packages.web import app, ext

cache = Cache(app, config={"CACHE_TYPE": "simple"})
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
    latest_projects = Project.objects.order_by("-released").limit(5)
    for package in Project.objects:
        classifier = package.classifiers
        if classifier and "topic" in classifier:
            topic = classifier["topic"]
            topic = topic.split("::")
            categories.add(topic[0].strip())

    return render_template(
        "index.html", principal_categories=categories, latest_projects=latest_projects
    )


@app.route("/project/<package_name>")
def package(package_name):
    package = Project.objects.get(name=package_name)
    maintainer = package["maintainer"]
    maintainer_packages = Project.objects(maintainer=maintainer)

    return render_template(
        "package.html", package=package, maintainer_packages=maintainer_packages
    )


ext.register_generator
def package_sitemap():
    for project in Project.objects.all():
        yield 'package', {'package_name': project.name}


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
