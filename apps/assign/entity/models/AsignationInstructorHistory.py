from django.db import models
from apps.assign.entity.models import AsignationInstructor

class AsignationInstructorHistory(models.Model):
    
    class Meta:
        db_table = 'asignation_instructor_history'
    
    asignation_instructor = models.ForeignKey(
        AsignationInstructor, on_delete=models.CASCADE, related_name="history"
    )
    old_instructor_id = models.IntegerField()
    message = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reasignación en {self.asignation_instructor.id} de instructor {self.old_instructor_id} el {self.date}"