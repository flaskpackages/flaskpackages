#!/usr/bin/env python

"""Tests for `flask_packages` package."""

from tests.factories import ProjectFactory


def test_index(app, client):
    ProjectFactory.create_batch(3)
    res = client.get("/")
    # Project.objects.insert(projects)
    assert res.status_code == 200
