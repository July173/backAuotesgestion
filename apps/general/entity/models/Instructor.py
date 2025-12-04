from django.db import models
from apps.security.entity.models import Person
from apps.general.entity.models.KnowledgeArea import KnowledgeArea


class Instructor(models.Model):
    
    class Meta:
        db_table = 'instructor'
    
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='instructor')  # Relación 1:1
    contract_type = models.ForeignKey('TypeContract', on_delete=models.PROTECT, related_name='instructors')
    knowledge_area = models.ForeignKey(KnowledgeArea, on_delete=models.PROTECT, related_name='instructors')
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    assigned_learners = models.IntegerField(null=True, blank=True)
    max_assigned_learners = models.IntegerField(null=True, blank=True, default=80)
    is_followup_instructor = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Instructor {self.id} - {self.knowledge_area.name}"
