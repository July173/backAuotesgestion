from django.db import models
from .LegalDocument import LegalDocument

class LegalSection(models.Model):
    
    class Meta:
        db_table = 'legal_section'
    
    document = models.ForeignKey(LegalDocument, on_delete=models.CASCADE, related_name='sections')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    order = models.IntegerField()
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"