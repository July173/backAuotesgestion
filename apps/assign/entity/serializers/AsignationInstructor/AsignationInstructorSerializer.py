from rest_framework import serializers
from apps.assign.entity.models import AsignationInstructor, RequestAsignation
from apps.general.entity.models import Instructor


class AsignationInstructorSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    request_asignation = serializers.PrimaryKeyRelatedField(queryset=RequestAsignation.objects.all())

    class Meta:
        model = AsignationInstructor
        ref_name = "AsignationInstructorSimpleSerializer"
        fields = [
            'id',
            'instructor',
            'request_asignation'
        ]
