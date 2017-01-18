"""
Abusor API client.

This file contains a simple client that is able to send new abuse events
to abusor using POST requests to the REST interface.
"""
import argparse
import sys
from datetime import datetime, timedelta, tzinfo

import requests


def parse_arguments():
    """Setup and handle command line arguments."""
    parser = argparse.ArgumentParser(description="Abusor API client")
    parser.add_argument('--ip', '-i', type=str, metavar='x.x.x.x',
                        help="The IP address to report")
    parser.add_argument('--subject', '-s', type=str,
                        help='The event subject')
    parser.add_argument('--uri', '-u', type=str, metavar='https://example.com',
                        help='The root URI of the abusor API',
                        default='http://admin:admin@localhost:8000')
    return parser.parse_args()


def timezone_aware_datetime():
    """Generate a timezone aware datetime object."""
    zero = timedelta(0)

    class UTC(tzinfo):
        def utcoffset(self, dt):
            return zero

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return zero

    return datetime.now(UTC())


def post_to_api(uri, ip_address, subject):
    """Send a new event to the API."""
    endpoint = uri.rstrip('/') + '/event/'
    payload = {
        'ip_address': ip_address,
        'subject': subject,
        'date': str(timezone_aware_datetime()),
    }
    resp = requests.post(endpoint, json=payload)
    if resp.status_code == 201:
        return
    else:
        sys.exit("Error while posting the event: [{}]: {}".format(
            resp.status_code, resp.content))


def main():
    """Main routine for the client."""
    args = parse_arguments()
    post_to_api(args.uri, args.ip, args.subject)

if __name__ == "__main__":
    main()
