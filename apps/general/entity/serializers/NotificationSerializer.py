from rest_framework import serializers
from apps.general.entity.models.Notification import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
