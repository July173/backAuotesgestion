from django.db import models

class Colors(models.Model):
    
    class Meta:
        
        db_table = 'base_colors'

    name = models.CharField(max_length=100)
    hexagonal_value = models.CharField(max_length=7)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.hexagonal_value})"

