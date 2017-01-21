import pytest
from faker import Faker
from pytest_django.lazy_django import skip_if_no_django
from pytest_factoryboy import register

from . import factories


# register factories as fixtures
register(factories.CaseFactory)
register(factories.EventFactory)


@pytest.fixture
def apiclient():
    """
    Return an API client instance.

    Based on the 'client' fixture in pytest-django.
    """
    skip_if_no_django()

    from rest_framework.test import APIClient  # noqa
    return APIClient()


@pytest.fixture
def fake():
    """Retrun an instance of the Faker library."""
    return Faker()
