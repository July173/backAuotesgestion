from django.db import models

class DocumentType(models.Model):
    class Meta:
        db_table = 'document_type'
    
    name = models.CharField(max_length=100)
    acronyms = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name