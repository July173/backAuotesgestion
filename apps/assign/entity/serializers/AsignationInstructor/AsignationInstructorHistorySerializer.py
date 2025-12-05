from rest_framework import serializers
from apps.assign.entity.models.AsignationInstructorHistory import AsignationInstructorHistory

class AsignationInstructorHistorySerializer(serializers.ModelSerializer):
    state_asignation = serializers.SerializerMethodField(read_only=True)

    def get_state_asignation(self, obj):
        try:
            return obj.asignation_instructor.state_asignation
        except Exception:
            return None
    class Meta:
        model = AsignationInstructorHistory
        fields = [
            'id',
            'asignation_instructor',
            'state_asignation',
            'old_instructor_id',
            'message',
            'date'
        ]
        read_only_fields = ['id', 'date', 'changed_by']
