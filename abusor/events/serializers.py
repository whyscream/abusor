from rest_framework import serializers

from .models import Case, Event


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="event-detail"
    )

    class Meta:
        model = Case
        fields = "__all__"
        read_only_fields = ("as_number", "country_code", "end_date", "score")


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("as_number", "country_code", "report_date", "score", "case")
