from rest_framework import serializers

class CreateApprenticeSerializer(serializers.Serializer):
    type_identification = serializers.IntegerField(required=True)
    number_identification = serializers.IntegerField(required=True)
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    ficha_id = serializers.IntegerField()