import json

import pytest
import responses

from abusor.client.abusor_api_client import parse_arguments, post_to_api

try:
    from django.urls import reverse
except ImportError:
    # for django < 1.10
    from django.core.urlresolvers import reverse


def test_post_to_api(fake, mock_resp):
    """Verify that the data is posted correctly to the Abusor API."""
    uri = fake.url().rstrip("/")
    token = fake.sha1()
    ip = fake.ipv4()
    subject = fake.sentence()

    # prepare the mock response
    endpoint = uri + reverse("event-list")
    mock_resp.add(responses.POST, endpoint, status=201)

    result = post_to_api(uri, token, ip, subject)
    assert result is None

    # inspect the performed request
    req = mock_resp.calls[-1].request
    assert "Authorization" in req.headers
    assert req.headers["Authorization"] == "Token {}".format(token)

    payload = json.loads(req.body.decode())
    assert "ip_address" in payload
    assert payload["ip_address"] == ip
    assert "subject" in payload
    assert payload["subject"] == subject


def test_post_to_api_error(fake, mock_resp):
    """Verify that an API error is reported correctly."""
    uri = fake.uri().rstrip("/")
    token = None
    ip = fake.ipv4()
    subject = fake.sentence()

    # prepare the mock response
    endpoint = uri + reverse("event-list")
    mock_resp.add(responses.POST, endpoint, body="No unauthorized access", status=401)

    with pytest.raises(SystemExit) as excinfo:
        post_to_api(uri, token, ip, subject)
    assert "[401]" in str(excinfo.value)
    assert "No unauthorized access" in str(excinfo.value)


def test_parse_arguments_subject_escaping(fake, monkeypatch):
    """Verify that subject escaping using double underscore works properly."""
    ip = fake.ipv4()
    subject = fake.sentence()
    assert " " in subject

    escaped_subject = subject.replace(" ", "__")
    assert " " not in escaped_subject

    monkeypatch.setattr(
        "sys.argv", ["progname", "--subject", escaped_subject, "--ip", ip]
    )
    args = parse_arguments()
    assert args.subject == subject


def test_parse_arguments_environment_vars(fake, monkeypatch):
    """Verify that we can set various arguments using environment vars."""
    uri = fake.uri().rstrip("/")
    token = fake.sha1()
    monkeypatch.setenv("ABUSOR_URI", uri)
    monkeypatch.setenv("ABUSOR_TOKEN", token)

    monkeypatch.setattr("sys.argv", ["progname", "-i", "1.2.3.4", "-s", "foo"])
    args = parse_arguments()
    assert args.uri == uri
    assert args.token == token
