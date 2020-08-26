import pytest
import mongoengine as me

from pathlib import Path

from flask_packages.web import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
