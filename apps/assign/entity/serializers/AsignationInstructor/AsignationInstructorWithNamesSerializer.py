from rest_framework import serializers

class PersonBasicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    second_name = serializers.CharField(allow_null=True, required=False)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(allow_null=True, required=False)
    number_identification = serializers.IntegerField()
    phone_number = serializers.IntegerField()
    type_identification = serializers.CharField(allow_null=True, required=False)
    active = serializers.BooleanField()

class AsignationInstructorWithNamesSerializer(serializers.Serializer):
    asignation_id = serializers.IntegerField()
    apprentice = PersonBasicSerializer()
    instructor = PersonBasicSerializer()
