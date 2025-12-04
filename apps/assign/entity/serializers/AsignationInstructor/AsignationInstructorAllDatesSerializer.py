from rest_framework import serializers
from apps.assign.entity.models import AsignationInstructor, RequestAsignation, Message
from apps.general.entity.models import Instructor
from apps.assign.entity.enums.request_state_enum import RequestState


class AsignationInstructorSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    request_asignation = serializers.PrimaryKeyRelatedField(queryset=RequestAsignation.objects.all())
    content = serializers.CharField(required=False, allow_blank=True, write_only=True)
    type_message = serializers.CharField(required=False, allow_blank=True, write_only=True)
    whose_message = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    request_state = serializers.ChoiceField(choices=[(choice.value, choice.label) for choice in RequestState], required=False, write_only=True)

    class Meta:
        model = AsignationInstructor
        ref_name = "AsignationInstructorWithMessageSerializer"
        fields = [
            'id',
            'instructor',
            'request_asignation',
            'content',
            'type_message',
            'whose_message',
            'request_state'
        ]
