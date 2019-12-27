import ipaddress
from unittest.mock import Mock, patch

import GeoIP

from abusor.events.utils import find_as_number, find_country_code

# a mocked geoip database object for use in tests
mock_geoip = Mock(spec=GeoIP.GeoIP)
mock_geoip.country_code_by_addr = Mock(return_value="NL")
mock_geoip.country_code_by_addr_v6 = Mock(return_value="BE")


@patch("abusor.events.utils.dns_lookup")
def test_find_as_number_ipv4(patched):
    """Verify that we can extract a correct AS number."""
    patched.return_value = ['"13335 | 104.16.0.0/12 | US | arin | 2014-03-28"']

    ip = ipaddress.ip_address("1.2.3.4")
    as_number = find_as_number(ip)
    assert as_number == 13335

    patched.assert_called_with("4.3.2.1.origin.asn.cymru.com.", "TXT")


@patch("abusor.events.utils.dns_lookup")
def test_find_as_number_ipv6(patched):
    """Verify that we can extract a correct AS number."""
    patched.return_value = ['"3265 | 2001:980::/29 | NL | ripencc | 2002-10-25"']

    ip = ipaddress.ip_address("2001:db8::1")
    as_number = find_as_number(ip)
    assert as_number == 3265

    patched.assert_called_with(
        "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.origin6.asn.cymru.com.",  # noqa: E501
        "TXT",
    )


@patch("abusor.events.utils.dns_lookup")
def test_find_as_number_no_result(patched, fake):
    """Verify that we can handle an empty result froma dns lookup."""
    patched.return_value = []

    ip = ipaddress.ip_address(fake.ipv4())
    as_number = find_as_number(ip)
    assert as_number is None


@patch("abusor.events.utils.dns_lookup")
def test_find_as_number_multiple(patched, fake):
    """Verify that we can handle a result with multiple AS numbers."""
    patched.return_value = ['"123 456 | 104.16.0.0/12 | US | arin | 2014-03-28"']

    ip = ipaddress.ip_address(fake.ipv4())
    as_number = find_as_number(ip)
    assert as_number == 123


@patch("GeoIP.open")
def test_find_country_code_ipv4(patched):
    """Verify that we can extract a country code."""
    patched.return_value = mock_geoip

    ip = ipaddress.ip_address("1.2.3.4")
    country_code = find_country_code(ip)
    assert country_code == "NL"


@patch("GeoIP.open")
def test_find_country_code_ipv6(patched):
    """Verify that we can extract a country code."""
    patched.return_value = mock_geoip

    ip = ipaddress.ip_address("2001:db8::1")
    country_code = find_country_code(ip)
    assert country_code == "BE"


@patch("GeoIP.open")
def test_find_country_code_no_result(patched, fake):
    """Verify that we can handle a Geoip error."""
    mock_geoip.country_code_by_addr = Mock(side_effect=GeoIP.error)
    patched.return_value = mock_geoip

    ip = ipaddress.ip_address(fake.ipv4())
    country_code = find_country_code(ip)
    assert country_code is None
