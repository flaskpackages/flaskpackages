#!/usr/bin/env python

"""Tests for `flask_packages` package."""

import unittest

from flask_packages import flask_packages
from tests.factories import ProjectFactory
from flask_packages.models import Project


def test_index(app, client):
    projects = ProjectFactory.create_batch(3)
    res = client.get('/')
    #Project.objects.insert(projects)
    assert res.status_code == 200
