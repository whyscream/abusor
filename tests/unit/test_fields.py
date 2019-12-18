import ipaddress

import pytest
from django.core.exceptions import ValidationError

from abusor.events.fields import GenericIPNetworkField


def test_ipnetwork_field_to_python(fake):
    """Check that the field returns proper python objects."""
    field = GenericIPNetworkField()
    ip_address = '192.0.2.42'
    ip_network = ipaddress.ip_network('192.0.2.42/32')

    assert field.to_python(ip_address) == ip_network
    assert field.to_python(ip_network) == ip_network

    with pytest.raises(ValidationError):
        field.to_python('192.0.2.42/29')

    with pytest.raises(ValidationError):
        field.to_python('aap')

    result = field.to_python(fake.ipv4())
    assert isinstance(result, ipaddress.IPv4Network)

    result = field.to_python(fake.ipv6())
    assert isinstance(result, ipaddress.IPv6Network)

    assert field.to_python(None) is None


def test_ipnetwork_field_get_prep_value(fake):
    """Verify that the field returns proper databse query values."""
    field = GenericIPNetworkField()

    result = field.get_prep_value(fake.ipv4())
    assert isinstance(result, str)

    ip_network = ipaddress.ip_network(fake.ipv4())
    result = field.get_prep_value(ip_network)
    assert isinstance(result, str)

    result = field.get_prep_value(fake.ipv6())
    assert isinstance(result, str)

    ip_network = ipaddress.ip_network(fake.ipv6())
    result = field.get_prep_value(ip_network)
    assert isinstance(result, str)
