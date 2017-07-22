import dns.resolver
from dns.exception import DNSException


def find_as_number(ip_address):
    """
    Lookup an AS number for the given ip address.

    The result is retrieved from the origin(6).asn.cymru.com DNS service.
    """
    if ip_address.version == 4:
        reverse = '.'.join(reversed(ip_address.exploded.split('.')))
        lookup = '.'.join([reverse, 'origin.asn.cymru.com'])
    elif ip_address.version == 6:
        reverse = '.'.join(reversed(ip_address.exploded.replace(':', '')))
        lookup = '.'.join([reverse, 'origin6.asn.cymru.com'])
    answers = dns_lookup(lookup, 'TXT')
    if not answers:
        return None
    txt = answers[0]
    # parse the format used by cymru: "13335 | 104.16.0.0/12 | US | arin | 2014-03-28"
    as_number, network, country, rir, date = [x.strip('" ') for x in txt.split('|')]
    return int(as_number)


def dns_lookup(lookup, type):
    """Perform a dns query, return a list of results."""
    results = []
    try:
        answers = dns.resolver.query(lookup, type)
    except DNSException:
        # ignore errors, just retun an empty result
        pass
    else:
        for rdata in answers:
            results.append(rdata.to_text())
    return results
