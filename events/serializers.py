from rest_framework import serializers

from .models import Case, Event


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='event-detail')
    class Meta:
        model = Case
        fields = '__all__'


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
