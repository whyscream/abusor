from events.models import Event


def test_event_str_formatting(random_ipv4, random_ipv6):
    """Verify default formatting of an Event when cast to string."""
    event = Event(ip_address=random_ipv4, subject='foo')
    result = str(event)
    assert "foo (" + random_ipv4 + ")" == result

    event.ip_address = random_ipv6
    result = str(event)
    assert "foo (" + random_ipv6 + ")" == result
