from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from .admin_helpers import RangeListFilter
from .models import Case, Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "subject",
        "date",
        "score",
        "actual_score",
        "has_case",
    )
    list_display_links = ("ip_address", "subject")
    search_fields = ("ip_address", "subject", "date", "report_date", "description")

    readonly_fields = ("report_date",)
    save_on_top = True

    def has_case(self, obj):
        """Whether a case is attached or not."""
        return bool(obj.case)

    has_case.boolean = True


class EventInline(admin.TabularInline):
    model = Event
    fields = ("date", "ip_address", "subject", "description", "score")
    readonly_fields = fields
    show_change_link = True
    extra = 0

    def has_add_permission(*args):
        """Hide the 'Add another event' button."""
        return False


class IsOpenListFilter(admin.SimpleListFilter):
    title = _("is open")
    parameter_name = "is_open"

    def lookups(self, request, model_admin):
        """Return the boolean options."""
        return (("true", _("Yes")), ("false", _("No")))

    def queryset(self, request, queryset):
        """Find out whether the case is open."""
        if self.value() == "true":
            return queryset.filter(end_date=None)
        if self.value() == "false":
            return queryset.exclude(end_date=None)


class NumberOfEventsListFilter(RangeListFilter):
    boundaries = (1, 5, 10, 20, 50, 100)
    title = _("number of events")
    parameter_name = "number_of_events"
    filter_on = "num_events"

    def queryset(self, request, queryset):
        """Annotate queryset with number of events."""
        queryset = queryset.annotate(num_events=Count("events"))
        return super().queryset(request, queryset)


class ScoreListFilter(RangeListFilter):
    boundaries = [0, 1, 5, 10, 50, 100, 200]
    title = _("score")
    parameter_name = "score"
    offset = 0.01


class CaseAdmin(admin.ModelAdmin):

    list_display = (
        "ip_network",
        "subject",
        "start_date",
        "number_of_events",
        "score",
        "is_open",
    )
    list_display_links = ("ip_network", "subject")
    list_filter = (
        IsOpenListFilter,
        "start_date",
        ScoreListFilter,
        NumberOfEventsListFilter,
    )
    search_fields = ("ip_network", "subject", "start_date", "description")

    inlines = (EventInline,)
    readonly_fields = ("start_date",)
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
