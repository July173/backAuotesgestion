from django.db import models

class TypeOfQueries(models.Model):

    class Meta:
        db_table = 'type_of_queries'

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
