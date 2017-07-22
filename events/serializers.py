import ipaddress

from rest_framework import serializers

from .models import Case, Event
from .utils import find_as_number


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='event-detail')

    class Meta:
        model = Case
        fields = '__all__'


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('as_number',)

    def create(self, validated_data):
        """Enhance with extra data before saving new objects."""
        ip = ipaddress.ip_address(validated_data['ip_address'])
        as_number = find_as_number(ip)
        validated_data['as_number'] = as_number
        return super().create(validated_data)
