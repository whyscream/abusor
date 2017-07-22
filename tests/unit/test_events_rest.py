from django.utils import timezone

import events.utils
from events.models import Event

try:
    from django.urls import reverse
except ImportError:
    # for django < 1.10
    from django.core.urlresolvers import reverse


def test_create_event(apiclient, admin_user, fake, monkeypatch):
    """Create an event through the API."""
    def mock_dns_lookup(lookup, type):
        return ['"13335 | 104.16.0.0/12 | US | arin | 2014-03-28"']
    monkeypatch.setattr(events.utils, 'dns_lookup', mock_dns_lookup)

    apiclient.force_authenticate(admin_user)
    date = timezone.now()
    ip = fake.ipv4()
    data = {
        'ip_address': ip,
        'date': date,
        'subject': 'my subject',
    }
    resp = apiclient.post(reverse('event-list'), data, format='json')
    assert resp.status_code == 201

    event = Event.objects.last()
    assert event.ip_address == ip
    assert event.date == date
    assert event.subject == 'my subject'
    assert event.as_number == 13335
