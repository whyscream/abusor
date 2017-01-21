from django.db import models
from django.utils import timezone


class Case(models.Model):
    """A collection of related abuse related events."""

    ip_address = models.GenericIPAddressField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """Default string representation."""
        if self.subject:
            return self.subject + " (" + self.ip_address + ")"
        return self.start_date.isoformat() + " (" + self.ip_address + ")"


class Event(models.Model):
    """An abuse related event."""

    LOGIN = 'login'
    MALWARE = 'malware'
    SPAM = 'spam'
    CATEGORY_CHOICES = (
        (LOGIN, 'Attempts to gain unauthorized access'),
        (MALWARE, 'Attempts to exploit software bugs'),
        (SPAM, 'Unsolicited bulk email sending')
    )

    ip_address = models.GenericIPAddressField()
    date = models.DateTimeField()
    subject = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)
    case = models.ForeignKey('Case', models.SET_NULL, blank=True, null=True, related_name='events')
    report_date = models.DateTimeField(default=timezone.now)
    external_reference = models.CharField(max_length=128, blank=True)

    def __str__(self):
        """Default string representation."""
        return self.subject + " (" + self.ip_address + ")"

    def find_related_case(self):
        """Find a case related to this event."""
        case = Case.objects.filter(ip_address=self.ip_address, end_date=None).order_by('start_date').last()
        if case:
            return case

        # no open case found, try closed ones
        case = Case.objects.filter(ip_address=self.ip_address, end_date__isnull=False).order_by('end_date').last()
        if case:
            return case
