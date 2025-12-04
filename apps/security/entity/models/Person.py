from django.db import models


class Person(models.Model):
    class Meta:
        db_table = 'person'

    type_identification = models.ForeignKey('DocumentType', on_delete=models.PROTECT, related_name='persons')
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, null=True, blank=True)
    first_last_name = models.CharField(max_length=100)
    second_last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.BigIntegerField()
    number_identification = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='personImages/', null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.first_last_name}"
