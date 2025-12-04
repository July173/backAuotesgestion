from django.db import models
from apps.security.entity.models import User

class Notification(models.Model):
    class Meta:
        db_table = 'notification'

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50)
    link = models.CharField(max_length=100, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.id_user}"
