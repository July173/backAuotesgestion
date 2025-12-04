from django.db import models
from apps.assign.entity.models import AsignationInstructor


class VisitFollowing(models.Model):

    class Meta:
        db_table = 'visit_following'

    asignation_instructor = models.ForeignKey(AsignationInstructor, on_delete=models.CASCADE, related_name='visits')
    visit_number = models.IntegerField()
    observations = models.TextField(max_length=500, null=True, blank=True)
    state_visit = models.CharField(max_length=50)
    scheduled_date = models.DateField()
    date_visit_made = models.DateField(null=True, blank=True)
    name_visit = models.CharField(max_length=100)
    observation_state_visit = models.TextField(max_length=500, null=True, blank=True)
    pdf_report = models.FileField(upload_to='visitReports/', null=True, blank=True)

    def __str__(self):
        return f"Visit {self.id} - {self.name_visit}"
