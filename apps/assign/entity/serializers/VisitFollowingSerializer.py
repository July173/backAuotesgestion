from rest_framework import serializers
from apps.assign.entity.models import VisitFollowing, AsignationInstructor


class VisitFollowingSerializer(serializers.ModelSerializer):
    asignation_instructor = serializers.PrimaryKeyRelatedField(queryset=AsignationInstructor.objects.all())
    state_asignation = serializers.SerializerMethodField(read_only=True)

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
            'pdf_report',
            'asignation_instructor',
            'state_asignation',
        ]
    
    def get_state_asignation(self, obj):
        if obj.asignation_instructor and hasattr(obj.asignation_instructor, 'state_asignation'):
            return obj.asignation_instructor.state_asignation
        return None
