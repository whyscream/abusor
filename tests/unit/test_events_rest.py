from django.urls import reverse
from django.utils import timezone

from events.models import Event


def test_create_event(apiclient, admin_user, fake):
    """Create an event through the API."""
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
