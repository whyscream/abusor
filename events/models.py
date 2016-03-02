from datetime import datetime

from django.db import models

class Case(models.Model):
    """A collection of related abuse related events."""
    ip_address = models.GenericIPAddressField()
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(blank=True)
    subject = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """Default string representation."""
        if self.subject:
            return self.ip_address + ": " + self.subject
        return self.ip_address + ": " + self.start_date.isoformat()

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
    case = models.ForeignKey('Case', models.SET_NULL, blank=True, null=True)
    report_date = models.DateTimeField(default=datetime.now)
    external_reference = models.CharField(max_length=128, blank=True)

    def __str__(self):
        """Default string representation."""
        if self.subject:
            return self.ip_address + ": " + self.subject
        return self.ip_address + ": " + self.date.isoformat()
