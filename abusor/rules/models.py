from django.db import models


class Rule(models.Model):
    class Meta:
        abstract = True

    requirement = models.CharField(max_length=32)
    requirement_param = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    action_kwargs = models.CharField(max_length=256, blank=True, default="")


class EventRule(Rule):
    pass


class CaseRule(Rule):
    pass
