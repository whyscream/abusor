from .models import Case


def find_related_case(event):
    """Try to find a Case related to the Event."""
    case = Case.objects.filter(ip_address=event.ip_address).order_by('start_date').last()
    if case:
        return case
