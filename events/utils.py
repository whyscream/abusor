

def find_related_case(event):
    """Try to find a Case related to the Event."""
    from .models import Case

    # find newest open case
    case = Case.objects.filter(ip_address=event.ip_address, end_date=None).order_by('start_date').last()
    if case:
        return case

    # no open case found, try closed ones
    case = Case.objects.filter(ip_address=event.ip_address, end_date__isnull=False).order_by('end_date').last()
    if case:
        return case
