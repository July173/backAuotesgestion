from rest_framework import serializers
from apps.assign.entity.models import VisitFollowing, AsignationInstructor


class VisitFollowingSerializer(serializers.ModelSerializer):
    asignation_instructor = serializers.PrimaryKeyRelatedField(queryset=AsignationInstructor.objects.all())
    request_asignation = serializers.SerializerMethodField(read_only=True)

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
            'request_asignation'
        ]
    
    def get_request_asignation(self, obj):
        """
        Obtiene el ID de la solicitud de asignación a través de la relación con AsignationInstructor.
        Este campo es de solo lectura y se incluye en las respuestas para referencia.
        """
        if obj.asignation_instructor and obj.asignation_instructor.request_asignation:
            return obj.asignation_instructor.request_asignation.id
        return None
