from django.contrib import admin

from .models import Event, Case


class EventAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'subject', 'date', 'score', 'has_case')
    list_display_links = ('ip_address', 'subject')
    readonly_fields = ('report_date',)

    def has_case(self, obj):
        """Whether a case is attached or not."""
        return bool(obj.case)
    has_case.boolean = True


class EventInline(admin.TabularInline):
    model = Event
    fields = ('date', 'ip_address', 'subject', 'description', 'score')
    readonly_fields = fields
    show_change_link = True
    extra = 0

    def has_add_permission(*args):
        """Hide the 'Add another event' button."""
        return False


class CaseAdmin(admin.ModelAdmin):

    list_display = ('ip_address', 'subject', 'start_date', 'number_of_events', 'score')
    list_display_links = ('ip_address', 'subject')

    readonly_fields = ('start_date', 'end_date')
    inlines = (EventInline,)

    def number_of_events(self, obj):
        """The number of events for the case."""
        return obj.events.count()

admin.site.register(Event, EventAdmin)
admin.site.register(Case, CaseAdmin)
