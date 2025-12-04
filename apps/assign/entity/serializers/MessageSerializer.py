from rest_framework import serializers
from apps.assign.entity.models.Message import Message

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['id', 'request_asignation', 'content', 'type_message', 'whose_message']
