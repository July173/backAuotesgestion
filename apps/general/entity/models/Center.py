from django.db import models

class Center(models.Model):
    
    class Meta:
        db_table = 'center'
    
    regional = models.ForeignKey('Regional', on_delete=models.CASCADE, related_name='centers')
    name = models.CharField(max_length=100)
    code_center = models.BigIntegerField(unique=True)
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.codeCenter})"
