from django.db import models

class Message(models.Model):

	class Meta:
		db_table = 'message'

	request_asignation = models.ForeignKey('assign.RequestAsignation',on_delete=models.CASCADE, related_name='messages')
	content = models.TextField(max_length=255)
	type_message = models.CharField(max_length=255)
	whose_message = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return f"Message {self.id} - {self.type_message}"
