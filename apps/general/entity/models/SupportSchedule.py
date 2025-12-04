from django.db import models

class SupportSchedule(models.Model):
    
    class Meta:
        db_table = 'support_schedule'
    
    day_range = models.CharField(max_length=100)
    hours = models.CharField(max_length=100)
    is_closed = models.BooleanField(default=False)
    notes = models.TextField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.day_range} ({'Closed' if self.is_closed else self.hours})"
