from django.db import models

class Boss(models.Model):
    class Meta:
        db_table = 'boss'
    # Nueva relación: Boss tiene FK a Enterprise para representar 1:N (una empresa, muchos jefes)
    enterprise = models.ForeignKey('assign.Enterprise', on_delete=models.CASCADE, related_name='bosses', null=True, blank=True)
    name_boss = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    email_boss = models.EmailField(max_length=100)
    position = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name_boss
