import json

import pytest
import responses
from django.urls import reverse

from client.abusor_api_client import post_to_api


def test_post_to_api(fake, mock_resp):
    """Verify that the data is posted correctly to the Abusor API."""
    uri = fake.url().rstrip('/')
    token = fake.sha1()
    ip = fake.ipv4()
    subject = fake.sentence()

    # prepare the mock response
    endpoint = uri + reverse('event-list')
    mock_resp.add(responses.POST, endpoint, status=201)

    result = post_to_api(uri, token, ip, subject)
    assert result is None

    # inspect the performed request
    req = mock_resp.calls[-1].request
    assert 'Authorization' in req.headers
    assert req.headers['Authorization'] == 'Token {}'.format(token)

    payload = json.loads(req.body.decode())
    assert 'ip_address' in payload
    assert payload['ip_address'] == ip
    assert 'subject' in payload
    assert payload['subject'] == subject


def test_post_to_api_error(fake, mock_resp):
    """Verify that an API error is reported correctly."""
    uri = fake.uri().rstrip('/')
    token = None
    ip = fake.ipv4()
    subject = fake.sentence()

    # prepare the mock response
    endpoint = uri + reverse('event-list')
    mock_resp.add(responses.POST, endpoint, body='No unauthorized access', status=401)

    with pytest.raises(SystemExit) as excinfo:
        post_to_api(uri, token, ip, subject)
    assert '[401]' in str(excinfo.value)
    assert 'No unauthorized access' in str(excinfo.value)
