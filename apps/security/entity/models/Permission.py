from django.db import models


class Permission(models.Model):
    class Meta:
        db_table = 'permission'
    
    type_permission = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    delete_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_permission
