from flask import render_template
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    auth_required
)
from flask_security.utils import (hash_password)
from flask_packages.web import app
from flask_packages.models import user_datastore

# Create a user to test with
@app.before_first_request
def create_user():
    #user_datastore.create_user(
    #        email="",
    #        password=hash_password(""))
    return

# Views
@app.route("/")
#@auth_required()
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                               