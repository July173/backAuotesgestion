from rest_framework import serializers
from apps.assign.entity.models import VisitFollowing


class VisitFollowingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitFollowing
        fields = [
            'observations',
            'state_visit',
            'date_visit_made',
            'observation_state_visit'
        ]