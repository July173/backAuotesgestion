from apps.security.entity.models import FormModule
from rest_framework import serializers


class FormModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormModule
        fields = ['id', 'form', 'module', ]
