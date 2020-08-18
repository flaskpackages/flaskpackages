
from flask_security import (
    UserMixin,
    RoleMixin
)
from flask_packages.web import app, db
from flask_security import Security, MongoEngineUserDatastore


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class user(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    fs_uniquifier = db.StringField(max_length=255)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


class Version(db.EmbeddedDocument):
    version = db.StringField()
    date = db.DateTimeField()
    link = db.StringField()
    sha256 = db.StringField()


class Classifier(db.EmbeddedDocument):
    development_status = db.ListField(db.StringField())
    programming_language = db.ListField(db.StringField())
    topic = db.ListField(db.StringField())
    framework = db.ListField(db.StringField())
    license = db.StringField()
    operating_system = db.StringField()
    environment = db.StringField()
    intended_audience = db.StringField()
    natural_language = db.StringField()
    typing = db.StringField()


class GithubStats(db.EmbeddedDocument):
    stars = db.IntField()
    open_pr = db.IntField()
    forks = db.IntField()


class Project(db.Document):
    meta = {'collection': 'flask_packages'}
    name = db.StringField(unique=True)
    description = db.StringField()
    lastest_version = db.StringField()
    maintainer = db.StringField()
    homepage = db.StringField()
    pypi_link = db.StringField(unique=True)

    versions = db.ListField(db.EmbeddedDocumentField(Version))
    github_stats = db.EmbeddedDocumentField(GithubStats)
    tags = db.ListField(db.StringField())
    classifiers = db.EmbeddedDocumentField(Classifier)

    released = db.DateTimeField()
    license = db.StringField()
    #category = db.ListField(db.Strin


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, user, Role)
security = Security(app, user_datastore)
