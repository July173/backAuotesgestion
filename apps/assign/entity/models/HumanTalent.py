from django.db import models


class HumanTalent(models.Model):

    class Meta:
        db_table = 'human_talent'

    enterprise = models.ForeignKey(
        'assign.Enterprise', on_delete=models.CASCADE, related_name='human_talent'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.BigIntegerField()
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
