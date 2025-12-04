from rest_framework import serializers
from apps.general.entity.models import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'code_program', 'name', 'description', 'active']
