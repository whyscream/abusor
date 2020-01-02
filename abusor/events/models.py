import ipaddress
import logging
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from .fields import GenericIPNetworkField

MAX_SCORE = Decimal("999.99")

logger = logging.getLogger(__name__)


class Case(models.Model):
    """A collection of related abuse related events."""

    class Meta:
        ordering = ("start_date",)

    ip_network = GenericIPNetworkField(blank=False)
    as_number = models.IntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))

    def __str__(self):
        return f"<Case {self.pk}>"

    def expand_network_prefix(self, prefixlen):
        """Expand the case to the given prefix length."""
        if self.ip_network.prefixlen < prefixlen:
            # prefix length equal or too low, don't do anything
            return False
        # calculate the new ip_network
        ip_network_str = f"{self.ip_network.network_address}/{prefixlen}"
        self.ip_network = ipaddress.ip_network(ip_network_str, strict=False)

        # find open cases in the new network, and merge them in.
        for case in Case.objects.filter(end_date=None).exclude(pk=self.pk):
            if self.ip_network.overlaps(case.ip_network):
                logger.debug(
                    f"Merged {case} into {self} while expanding network prefix."
                )
                case.events.all().update(case=self)
                case.close()
                case.save()
        # get the score from the new events
        self.recalculate_score()
        return True

    def recalculate_score(self):
        """Recalculate Case score from actual Event scores."""
        if self.end_date:
            return

        scores = []
        for event in self.events.all():
            scores.append(event.actual_score)

        self.score = Decimal(str(round(sum(scores), 2)))
        if self.score > MAX_SCORE:
            logger.warning(
                "Score {:f} for case {:d} exceeds MAX_SCORE, capped".format(
                    self.score, self.pk
                )
            )
            self.score = MAX_SCORE
        return self.score

    def close(self, *args):
        """Close the case.

        TOOD: remove this method as soon as we don't need it anymore for
        expand_network_prefix()..
        """
        self.recalculate_score()
        self.end_date = timezone.now()
        return True


class Event(models.Model):
    """An abuse related event."""

    class Meta:
        ordering = ("date",)

    LOGIN = "login"
    MALWARE = "malware"
    SPAM = "spam"
    CATEGORY_CHOICES = (
        (LOGIN, "Attempts to gain unauthorized access"),
        (MALWARE, "Attempts to exploit software bugs"),
        (SPAM, "Unsolicited bulk email sending"),
    )

    ip_address = models.GenericIPAddressField()
    as_number = models.IntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True)
    date = models.DateTimeField()
    subject = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)
    case = models.ForeignKey(
        "Case", models.SET_NULL, blank=True, null=True, related_name="events"
    )
    report_date = models.DateTimeField(default=timezone.now)
    external_reference = models.CharField(max_length=128, blank=True)

    @property
    def actual_score(self):
        """Calculate the current score based on the original score and the age."""
        diff = timezone.now() - self.date
        score = float(self.score) * settings.ABUSOR_SCORE_DECAY ** diff.days
        return round(score, 2)

    def __str__(self):
        return f"<Event {self.pk}>"

    def find_related_case(self):
        """Find a case related to this event."""
        event_network = ipaddress.ip_network(self.ip_address)
        for case in Case.objects.filter(end_date=None).order_by("-start_date"):
            if case.ip_network.overlaps(event_network):
                return case

    def get_or_create_case(self):
        if not self.case:
            case = self.find_related_case()
            if not case:
                case = Case.objects.create(
                    ip_network=ipaddress.ip_network(self.ip_address),
                    as_number=self.as_number,
                    country_code=self.country_code,
                    subject=self.subject,
                    start_date=self.report_date,
                )
                logger.info(f"Created new {case} related to {self}.")
            self.case = case
            self.save()
        return self.case
