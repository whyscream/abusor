from django.contrib import admin

from .models import Event, Case


class CaseAdmin(admin.ModelAdmin):

    list_display = ('ip_address', 'subject', 'start_date', 'number_of_events', 'score')
    list_display_links = ('ip_address', 'subject')

    def number_of_events(self, obj):
        """The number of events for the case."""
        return obj.events.count()

admin.site.register(Event)
admin.site.register(Case, CaseAdmin)
