from django.contrib import admin

from .models import CaseRule, EventRule


class CaseRuleAdmin(admin.ModelAdmin):
    pass


class EventRuleAdmin(admin.ModelAdmin):
    pass


admin.site.register(CaseRule, CaseRuleAdmin)
admin.site.register(EventRule, EventRuleAdmin)
