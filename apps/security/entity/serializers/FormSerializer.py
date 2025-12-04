from apps.security.entity.models import Form
from rest_framework import serializers


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name', 'path', 'description', 'active']
