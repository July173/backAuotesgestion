from django.db import models


class Ficha(models.Model):
    
    class Meta:
        db_table = 'ficha'
    
    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='fichas')
    file_number = models.BigIntegerField(unique=True)
    type_modality = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ficha {self.file_number}"
