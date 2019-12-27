from django.contrib import admin


class RangeListFilter(admin.SimpleListFilter):
    """Simple ListFilter base for filtering on numeric ranges."""

    separator = "-"
    boundaries = None
    filter_on = None
    offset = 1

    def __init__(self, request, params, model, model_admin):
        """Check for mandatory settings."""
        super().__init__(request, params, model, model_admin)
        if self.boundaries is None or len(self.boundaries) < 2:
            raise ValueError(
                "The range filter '{}' does not specify at least "
                "2 items in 'boundaries'.".format(self.__class__.__name__)
            )
        if self.filter_on is None:
            self.filter_on = self.parameter_name

    def lookups(self, request, model_admin):
        """Return a set choices to filter on based on the boundaries."""
        start = None
        for value in self.boundaries:
            if start is None:
                start = value
                # move on to the next value
                continue

            raw = "{}{}{}".format(start, self.separator, value)
            formatted = "{} to {}".format(start, value)
            start = value + self.offset
            yield (raw, formatted)

    def queryset(self, request, queryset):
        """Filter based on the range given."""
        if not self.value() or self.separator not in self.value():
            return queryset
        (low, high) = self.value().split(self.separator)
        if low:
            filter_expr = "{}__gte".format(self.filter_on)
            queryset = queryset.filter(**{filter_expr: low})
        if high:
            filter_expr = "{}__lte".format(self.filter_on)
            queryset = queryset.filter(**{filter_expr: high})
        return queryset
