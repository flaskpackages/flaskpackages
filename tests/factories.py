import datetime

import factory
from factory.fuzzy import FuzzyDateTime

from flask_packages.models import Project

faker = factory.faker.Faker._get_faker()


class ProjectFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Project

    name = factory.LazyFunction(faker.company)
    pypi_link = factory.LazyFunction(faker.url)
    released = FuzzyDateTime(
        datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2015, 12, 31, 20, tzinfo=datetime.timezone.utc),
    )
