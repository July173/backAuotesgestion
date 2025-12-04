from django.db import models


class Enterprise(models.Model):
    class Meta:
        db_table = 'enterprise'
    # Antes: boss era OneToOne en Enterprise.
    # Ahora la relación es 1:N: varios Boss pueden pertenecer a una Enterprise.
    name_enterprise = models.CharField(max_length=100)
    locate = models.CharField(max_length=255)
    nit_enterprise = models.CharField(max_length=20)
    email_enterprise = models.EmailField(max_length=100)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name_enterprise
