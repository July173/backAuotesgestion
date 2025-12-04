from rest_framework import serializers
from apps.assign.entity.models import Boss, Enterprise


class BossSerializer(serializers.ModelSerializer):
    enterprise = serializers.PrimaryKeyRelatedField(queryset=Enterprise.objects.all())

    class Meta:
        model = Boss
        fields = [
            'id',
            'enterprise',
            'name_boss',
            'phone_number',
            'email_boss',
            'position',
            'active'
        ]
