from rest_framework import serializers
from apps.assign.entity.models import AsignationInstructor
from apps.security.entity.models import Person

class PersonBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id', 'first_name', 'second_name', 'first_last_name', 'second_last_name',
            'number_identification', 'phone_number', 'type_identification', 'active'
        ]

class AsignationInstructorFullDataSerializer(serializers.Serializer):
    asignation = serializers.PrimaryKeyRelatedField(read_only=True)
    apprentice = PersonBasicSerializer(read_only=True)
    instructor = PersonBasicSerializer(read_only=True)
