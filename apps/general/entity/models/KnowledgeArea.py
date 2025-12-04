from django.db import models


class KnowledgeArea(models.Model):
    
    class Meta:
        db_table = 'knowledge_area'
    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
