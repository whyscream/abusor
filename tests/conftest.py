from random import randrange

import pytest
from pytest_django.lazy_django import skip_if_no_django


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
def random_ipv4():
    """Return a random ipv4 address."""
    octets = (
        '127',
        str(randrange(0, 255)),
        str(randrange(0, 255)),
        str(randrange(0, 255)),
    )
    return ".".join(octets)


@pytest.fixture
def random_ipv6():
    """Return a random ipv6 address."""
    # num_octets = randrange(3, 8)
    octets = [
        '2001',
        'db8',
        hex(randrange(0, 65535))[2:],
        hex(randrange(0, 65535))[2:],
        hex(randrange(0, 65535))[2:],
    ]
    return ":".join(octets) + "::"
