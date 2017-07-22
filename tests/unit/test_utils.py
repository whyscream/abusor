import ipaddress

import events.utils as utils


def test_find_as_number_ipv4(fake, monkeypatch):
    """Verify that we can extract a correct AS number."""
    def mock_dns_lookup(lookup, type):
        return ['"13335 | 104.16.0.0/12 | US | arin | 2014-03-28"']
    monkeypatch.setattr(utils, 'dns_lookup', mock_dns_lookup)

    ip = ipaddress.ip_address(fake.ipv4())
    as_number = utils.find_as_number(ip)
    assert as_number == 13335


def test_find_as_number_ipv6(fake, monkeypatch):
    """Verify that we can extract a correct AS number."""
    def mock_dns_lookup(lookup, type):
        return ['"3265 | 2001:980::/29 | NL | ripencc | 2002-10-25"']
    monkeypatch.setattr(utils, 'dns_lookup', mock_dns_lookup)

    ip = ipaddress.ip_address(fake.ipv6())
    as_number = utils.find_as_number(ip)
    assert as_number == 3265


def test_find_as_number_no_result(fake, monkeypatch):
    """Verify that we can handle an empty result froma dns lookup."""
    def mock_dns_lookup(lookup, type):
        return []
    monkeypatch.setattr(utils, 'dns_lookup', mock_dns_lookup)

    ip = ipaddress.ip_address(fake.ipv4())
    as_number = utils.find_as_number(ip)
    assert as_number is None
