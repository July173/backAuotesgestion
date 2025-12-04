from rest_framework import serializers
from apps.security.entity.serializers.FormItemSerializer import FormItemSerializer


class MenuFormSerializer(serializers.Serializer):
    name = serializers.CharField()
    form = FormItemSerializer(many=True)
