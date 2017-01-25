from django.conf import settings
from django.db import models
from django.utils import timezone

from .rules import apply_effect, check_requirement


class Case(models.Model):
    """A collection of related abuse related events."""

    ip_address = models.GenericIPAddressField()
    netmask = models.CharField(max_length=3, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        """Default string representation."""
        detail = self.subject if self.subject else self.start_date.isoformat()
        return "{} ({})".format(detail, self.ip_address)

    def recalculate_score(self):
        """Recalculate Case score from actual Event scores."""
        if self.end_date:
            return

        scores = []
        for event in self.events.all():
            scores.append(event.actual_score)

        self.score = round(sum(scores), 2)
        return self.score

    def close(self, *args):
        """Close the case."""
        self.recalculate_score()
        self.end_date = timezone.now()

    def apply_business_rules(self):
        """Apply business rules on the case."""
        self.recalculate_score()

        for rule in settings.ABUSOR_CASE_RULES:
            result = check_requirement(self, rule['when'])
            if result:
                apply_effect(self, rule['then'])
        self.save()


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

    @property
    def actual_score(self):
        """Calculate the current score based on the original score and the age."""
        diff = timezone.now() - self.report_date
        score = float(self.score) * settings.ABUSOR_SCORE_DECAY**diff.days
        return round(score, 2)

    def __str__(self):
        """Default string representation."""
        return "{} ({})".format(self.subject, self.ip_address)

    def find_related_case(self):
        """Find a case related to this event."""
        case = Case.objects.filter(ip_address=self.ip_address, end_date=None).order_by('start_date').last()
        if case:
            return case

        # no open case found, try closed ones
        case = Case.objects.filter(ip_address=self.ip_address, end_date__isnull=False).order_by('end_date').last()
        if case:
            return case

    def apply_business_rules(self):
        """Find applicable business rules and apply them to the Event."""
        if not self.case:
            case = self.find_related_case()
            if not case:
                create_data = {
                    'ip_address': self.ip_address,
                    'subject': self.subject,
                    'start_date': self.report_date,
                }
                case = Case.objects.create(**create_data)
            self.case = case

        for rule in settings.ABUSOR_EVENT_RULES:
            result = check_requirement(self, rule['when'])
            if result:
                apply_effect(self, rule['then'])
        self.save()
