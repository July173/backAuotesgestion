from rest_framework import serializers

class ReasignationInstructorSerializer(serializers.Serializer):
	asignation_instructor = serializers.IntegerField(required=True)
	new_instructor_id = serializers.IntegerField(required=True)
	message = serializers.CharField(required=True, allow_blank=False, max_length=500)
