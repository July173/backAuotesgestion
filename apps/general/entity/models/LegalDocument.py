from django.db import models

class LegalDocument(models.Model):
    
    class Meta:
        db_table = 'legal_document'
    
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    effective_date = models.DateField()
    last_update = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.type})"
