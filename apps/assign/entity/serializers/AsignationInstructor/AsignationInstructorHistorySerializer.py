from rest_framework import serializers
from apps.assign.entity.models.AsignationInstructorHistory import AsignationInstructorHistory

class AsignationInstructorHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignationInstructorHistory
        fields = [
            'id',
            'asignation_instructor',
            'old_instructor_id',
            'message',
            'date'
        ]
        read_only_fields = ['id', 'date', 'changed_by']
