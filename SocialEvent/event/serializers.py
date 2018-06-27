from rest_framework import serializers
from event.models import *


class EventGeneralSerializer(serializers.ModelSerializer):
    photopaths = serializers.StringRelatedField(many=True)
    class Meta:
        model = EventGeneral
        fields = ('id', 'title', 'photopaths', 'start_date', 'end_date', 'number_like', 'c_id', 'date_created')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('visitor_id', 'event_id', 'content', 'date_commented')

class ParticipateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participate
        fields = ('visitor_id', 'event_id')