from django.db.models import Count
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Event, Case


class EventAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'subject', 'date', 'score', 'actual_score', 'has_case')
    list_display_links = ('ip_address', 'subject')
    search_fields = ('ip_address', 'subject', 'date', 'report_date', 'description')

    readonly_fields = ('report_date',)
    save_on_top = True

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


class NumberOfEventsFilter(admin.SimpleListFilter):
    title = _('number of events')
    parameter_name = 'number_of_events'
    _separator = '-'

    def lookups(self, request, model_admin):
        """Return a tuple of choices to filter on."""
        boundaries = [5, 10, 20, 50, 100]
        start = 1
        for pos, value in enumerate(boundaries):
            key = '{}{}{}'.format(start, self._separator, value)
            display = '{} to {}'.format(start, value)
            start = value + 1
            yield (key, display)

    def queryset(self, request, queryset):
        """Filter based on number of events."""
        if not self.value() or self._separator not in self.value():
            return queryset
        # annotate qs with number of events
        queryset = queryset.annotate(num_events=Count('events'))
        (lower, higher) = self.value().split(self._separator)
        if lower:
            queryset = queryset.filter(num_events__gte=lower)
        if higher:
            queryset = queryset.filter(num_events__lte=higher)
        return queryset


class CaseAdmin(admin.ModelAdmin):

    list_display = ('ip_address', 'subject', 'start_date', 'number_of_events', 'score', 'is_open')
    list_display_links = ('ip_address', 'subject')
    list_filter = ('start_date', 'score', NumberOfEventsFilter)
    search_fields = ('ip_address', 'subject', 'start_date', 'description')

    inlines = (EventInline,)
    readonly_fields = ('start_date',)
    save_on_top = True

    def number_of_events(self, obj):
        """The number of events for the case."""
        return obj.events.count()

    def is_open(self, obj):
        """Whether the case is open or closed."""
        return obj.end_date is None
    is_open.boolean = True

admin.site.register(Event, EventAdmin)
admin.site.register(Case, CaseAdmin)
