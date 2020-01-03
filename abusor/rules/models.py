from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from abusor.events.models import Case

from .plugins import PluginError
from .processing import apply_requirement


class Rule(models.Model):
    class Meta:
        abstract = True

    requirement = models.CharField(max_length=32)
    requirement_param = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    action_kwargs = models.CharField(max_length=256, blank=True, default="")


class EventRule(Rule):
    def __str__(self):
        return f"<EventRule {self.pk}>"


class CaseRule(Rule):
    def __str__(self):
        return f"<CaseRule {self.pk}>"

    def clean(self):
        """Validate the rule, checking params with the picked requirement and action."""

        case = Case()
        try:
            apply_requirement(case, self.requirement, self.requirement_param)
        except PluginError as err:
            raise ValidationError({"requirement_param": _(str(err))})
