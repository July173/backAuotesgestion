from rest_framework import serializers
from apps.assign.entity.models import HumanTalent, Enterprise


class HumanTalentSerializer(serializers.ModelSerializer):
    enterprise = serializers.PrimaryKeyRelatedField(queryset=Enterprise.objects.all())

    class Meta:
        model = HumanTalent
        fields = [
            'id',
            'enterprise',
            'name',
            'email',
            'phone_number',
            'active'
        ]
