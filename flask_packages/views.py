from flask import render_template, send_from_directory
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    auth_required
)
from flask_security.utils import (hash_password)
from flask_packages.web import app, db
from flask_packages.models import user_datastore

from flask_mongoengine import MongoEngine
import mongoengine as me
import os

# Create a user to test with
@app.before_first_request
def create_user():
    #user_datastore.create_user(
    #        email="admin@admin.com",
    #        password=hash_password("admin"))
    return

# Views
@app.route("/")
@auth_required()
def home():
    principal_categories = navbar()
    return render_template('index.html', principal_categories=principal_categories)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                               
class flask_collection(me.Document):
    name = me.StringField(required=True)
    project_url = me.StringField()
    maintainer = me.StringField()
    description = me.StringField()
    classifiers = me.StringField()
    homepage = me.StringField()
    released = me.StringField()
    versions = me.StringField()
    lastest_version = me.StringField()
    pypi_link = me.StringField()


def navbar(): 
    # Insert data to db
    #bttf = user(email="test")
    #bttf.email = flask_collection(password="tt0088763")
    #bttf.save()

    # Getting one element printed (eg. print password from email admin@me.com)
    #some_theron_movie = flask_collection.objects(name="tessera-client").first()
    #print(some_theron_movie.description)

    # Getting all elements printed out from a Query (eg. Bring all passwords for accounts with email admin@me.com)
    #some_theron_movie = flask_collection.objects(name="tessera-client")
    #for item in some_theron_movie:
    #    print(item.maintainer)

    # Getting item from all documents (eg. print name from all packages)
    categorie0 = []
    categorie1 = []
    categorie2 = []
    categorie3 = []
    for package in flask_collection.objects:
        classifier = package.classifiers
        try:
            topics = classifier['Topic']
            for topic in topics:
                topic = topic.split("::")
                categorie0.append(topic[0].strip())
                categorie1.append(str(topic[0]+'::'+topic[1]))
                categorie2.append(str(topic[0]+'::'+topic[1]+'::'+topic[2]))
                categorie3.append(str(topic[0]+'::'+topic[1]+'::'+topic[2]+'::'+topic[3]))
        except:
            a=2
    categorie0 = list(set(categorie0))
    categorie1 = list(set(categorie1))
    categorie2 = list(set(categorie2))
    categorie3 = list(set(categorie3))
    return categorie0
    #return render_template('test.html', categorie0=categorie0, categorie1=categorie1, categorie2=categorie2, categorie3=categorie3)
