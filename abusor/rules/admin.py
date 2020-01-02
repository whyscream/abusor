from django import forms
from django.contrib import admin

from .models import CaseRule, EventRule
from .processing import actions, requirements

action_choices = [(x.name, x.name) for x in actions]
requirement_choices = [(x.name, x.name) for x in requirements]


class CaseRuleAdminForm(forms.ModelForm):
    class Meta:
        model = CaseRule
        fields = "__all__"
        widgets = {
            "requirement": forms.Select(choices=requirement_choices),
            "action": forms.Select(choices=action_choices),
        }


class CaseRuleAdmin(admin.ModelAdmin):
    form = CaseRuleAdminForm


class EventRuleAdminForm(forms.ModelForm):
    class Meta:
        model = EventRule
        fields = "__all__"
        widgets = {
            "requirement": forms.Select(choices=requirement_choices),
            "action": forms.Select(choices=action_choices),
        }


class EventRuleAdmin(admin.ModelAdmin):
    form = EventRuleAdminForm


admin.site.register(CaseRule, CaseRuleAdmin)
admin.site.register(EventRule, EventRuleAdmin)
