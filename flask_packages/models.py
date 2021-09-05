from flask_security import MongoEngineUserDatastore, RoleMixin, Security, UserMixin

from flask_packages.web import app, db


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
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
    development_status = db.StringField()
    programming_language = db.StringField()
    topic = db.ListField(db.StringField())
    framework = db.StringField()
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
    meta = {"collection": "flask_packages"}
    name = db.StringField(unique=True, null=False)
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

    topics = db.ListField(db.StringField())


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)
