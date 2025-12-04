from rest_framework import serializers
from apps.general.entity.models.SupportSchedule import SupportSchedule

class SupportScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportSchedule
        fields = ['id', 'day_range', 'hours', 'is_closed', 'notes', 'active']
