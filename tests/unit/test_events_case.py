from datetime import datetime

from events.models import Case


def test_case_str_formatting(random_ipv4, random_ipv6):
    """Verify default formatting of a Case when cast to string."""
    case = Case(ip_address=random_ipv4)
    result = str(case)
    assert random_ipv4 in result
    assert datetime.now().strftime("%Y-%m-%d") in result

    case.ip_address = random_ipv6
    result = str(case)
    assert random_ipv6 in result

    case.subject = 'foo bar'
    result = str(case)
    assert "foo bar (" + random_ipv6 + ")" == result
