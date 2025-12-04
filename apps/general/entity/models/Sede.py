from django.db import models


class Sede(models.Model):

    class Meta:
        db_table = 'sede'

    center = models.ForeignKey('Center', on_delete=models.CASCADE, related_name='sedes')  # <-- Relación agregada
    name = models.CharField(max_length=100)
    code_sede = models.BigIntegerField(unique=True)
    address = models.CharField(max_length=255)
    phone_sede = models.BigIntegerField()
    email_contact = models.EmailField(max_length=100)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code_sede})"
