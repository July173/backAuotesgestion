from django.db import models


class Program(models.Model):

    class Meta:
        db_table = 'program'
        
    name = models.CharField(max_length=100)
    code_program = models.BigIntegerField()
    description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code_program})"
