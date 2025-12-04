from rest_framework import serializers

class FormItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    path = serializers.CharField()
