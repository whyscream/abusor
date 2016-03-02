from django.db import models


class Case(models.Model):
    """A collection of related abuse related events."""
    ip_address = models.GenericIPAddressField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    summary = models.TextField()


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
    description = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    case = models.ForeignKey('Case', models.SET_NULL, blank=True, null=True)
    report_date = models.DateTimeField()
    external_reference = models.CharField(max_length=128)
