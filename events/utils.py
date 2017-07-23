import logging

import dns.resolver
import GeoIP
from dns.exception import DNSException

# default install paths on ubuntu
GEOIP_IPV4_COUNTRY_DATABASE = '/usr/share/GeoIP/GeoIP.dat'
GEOIP_IPV6_COUNTRY_DATABASE = '/usr/share/GeoIP/GeoIPv6.dat'

# containers for cached database objects
GEOIP_IPV4_CACHE = None
GEOIP_IPV6_CACHE = None

logger = logging.getLogger(__name__)


def find_as_number(ip_address):
    """
    Lookup an AS number for the given ip address.

    The result is retrieved from the origin(6).asn.cymru.com DNS service.
    """
    if ip_address.version == 4:
        reverse = '.'.join(reversed(ip_address.exploded.split('.')))
        lookup = '.'.join([reverse, 'origin.asn.cymru.com.'])
    elif ip_address.version == 6:
        reverse = '.'.join(reversed(ip_address.exploded.replace(':', '')))
        lookup = '.'.join([reverse, 'origin6.asn.cymru.com.'])
    answers = dns_lookup(lookup, 'TXT')
    if not answers:
        return None
    txt = answers[0]
    # parse the format used by cymru: "13335 | 104.16.0.0/12 | US | arin | 2014-03-28"
    as_number, network, country, rir, date = [x.strip('" ') for x in txt.split('|')]
    if ' ' in as_number:
        # sometimes multiple AS numbers announce the ip (multihoming), just pick one
        as_number = as_number.split(' ')[0]
    return int(as_number)


def find_country_code(ip_address):
    """Lookup a iso3166 (two-letter) country code for the given ip address.

    The result is retrieved using a geoip legacy database.
    """
    global GEOIP_IPV4_CACHE, GEOIP_IPV6_CACHE
    try:
        if ip_address.version == 4:
            if not GEOIP_IPV4_CACHE:
                GEOIP_IPV4_CACHE = GeoIP.open(GEOIP_IPV4_COUNTRY_DATABASE, GeoIP.GEOIP_STANDARD)
            country_code = GEOIP_IPV4_CACHE.country_code_by_addr(ip_address.compressed)
        elif ip_address.version == 6:
            if not GEOIP_IPV6_CACHE:
                GEOIP_IPV6_CACHE = GeoIP.open(GEOIP_IPV6_COUNTRY_DATABASE, GeoIP.GEOIP_STANDARD)
            country_code = GEOIP_IPV6_CACHE.country_code_by_addr_v6(ip_address.compressed)
    except GeoIP.error as err:
        logger.warn('GeoIP lookup failed with an error: {}'.format(err))
        return None
    else:
        return country_code


def dns_lookup(lookup, type):
    """Perform a dns query, return a list of results."""
    results = []
    try:
        answers = dns.resolver.query(lookup, type)
    except DNSException as err:
        logger.warning('DNS lookup failed with an error: {}'.format(err))
        pass
    else:
        for rdata in answers:
            results.append(rdata.to_text())
    return results
