import ipaddress

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class GenericIPNetworkField(models.CharField):

    description = "An IP network"

    def __init__(self, *args, **kwargs):
        """Create new field, set max_length for ip networks."""
        kwargs['max_length'] = 49
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Deconstruct the field, remove max length value."""
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        """Convert input into a python IPv[4,6]Network object."""
        return self.to_python(value)

    def to_python(self, value):
        """Convert input into a python IPv[4,6]Network object."""
        if isinstance(value, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            return value

        if value is None:
            return value

        try:
            return ipaddress.ip_network(value)
        except ValueError:
            raise ValidationError(_("Invalid input for an IP network."))

    def get_prep_value(self, value):
        """Convert a python object into a database query value (i.e. a string)."""
        return str(value)
