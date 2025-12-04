from rest_framework import serializers
from apps.assign.entity.models import VisitFollowing, AsignationInstructor


class VisitFollowingSerializer(serializers.ModelSerializer):
    asignation_instructor = serializers.PrimaryKeyRelatedField(queryset=AsignationInstructor.objects.all())

    class Meta:
        model = VisitFollowing
        fields = [
            'id',
            'visit_number',
            'observations',
            'state_visit',
            'scheduled_date',
            'date_visit_made',
            'name_visit',
            'observation_state_visit',
            'asignation_instructor'
        ]
