from rest_framework import serializers
from apps.general.entity.models.SupportContact import SupportContact

class SupportContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportContact
        fields = ['id', 'type', 'label', 'value', 'extra_info', 'active']
