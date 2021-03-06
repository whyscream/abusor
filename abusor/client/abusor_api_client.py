#!/usr/bin/env python3
"""
Abusor API client.

This file contains a simple client that is able to send new abuse events
to abusor using POST requests to the REST interface.
"""
import argparse
import os
import sys
from datetime import datetime, timedelta, tzinfo
from textwrap import dedent

import requests


def parse_arguments():
    """Setup and handle command line arguments."""
    default_uri = "http://localhost:8000"
    epilog = dedent(
        """\
        The --token and --uri args can also be set using environment variables,
        when you don't want the values to be visible in the output of 'ps' etc.
        To use this, set the ABUSOR_TOKEN and ABUSOR_URI environment variables.

        The --subject argument may contain spaces. When your environment does not
        allow you to use these, it's possible to 'escape' the spaces by replacing
        them by double underscores (__). The client will 'unescape' these into
        spaces before posting your data."""
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Abusor API client",
        epilog=epilog,
    )
    parser.add_argument(
        "--ip",
        "-i",
        type=str,
        metavar="x.x.x.x",
        required=True,
        help="The IPv4 or IPv6 address to report",
    )
    parser.add_argument(
        "--subject", "-s", type=str, required=True, help="The event subject"
    )
    parser.add_argument("--token", "-t", type=str, help="The API authorization token")
    parser.add_argument(
        "--uri",
        "-u",
        type=str,
        metavar="https://example.com",
        help="The root URI of the abusor API",
        default=default_uri,
    )
    args = parser.parse_args()

    # extract args from environment
    if args.uri == default_uri:
        args.uri = os.environ.get("ABUSOR_URI", default_uri)
    if not args.token:
        args.token = os.environ.get("ABUSOR_TOKEN")

    if args.subject:
        args.subject = args.subject.replace("__", " ")
    return args


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


def post_to_api(uri, token, ip_address, subject):
    """Send a new event to the API."""
    endpoint = uri.rstrip("/") + "/api/event/"
    headers = {}
    if token:
        headers["Authorization"] = "Token {}".format(token)
    payload = {
        "ip_address": ip_address,
        "subject": subject,
        "date": str(timezone_aware_datetime()),
    }
    resp = requests.post(endpoint, headers=headers, json=payload)
    if resp.status_code == 201:
        return
    else:
        sys.exit(
            "Error while posting the event: [{}]: {}".format(
                resp.status_code, resp.content
            )
        )


def main():
    """Main routine for the client."""
    args = parse_arguments()
    post_to_api(args.uri, args.token, args.ip, args.subject)


if __name__ == "__main__":
    main()
