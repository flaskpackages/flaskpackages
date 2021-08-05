import os
from pathlib import Path

from flask_mongoengine import MongoEngine
from flask_sitemap import Sitemap

from flask_packages.app import create_app

template_folder = Path(os.path.dirname(__file__)) / "templates"

app = create_app(template_folder)
ext = Sitemap(app=app)
# Create database connection object
db = MongoEngine(app)


from flask_packages.views import *  # noqa
