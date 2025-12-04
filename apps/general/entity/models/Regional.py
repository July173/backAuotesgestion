from django.db import models


class Regional(models.Model):

    class Meta:
        db_table = 'regional'

    name = models.CharField(max_length=100)
    code_regional = models.BigIntegerField(unique=True)
    description = models.TextField(max_length=255)
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.codeRegional})"
