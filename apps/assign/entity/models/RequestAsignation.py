from django.db import models
from apps.general.entity.models import Apprentice
from apps.assign.entity.enums.request_state_enum import RequestState


class RequestAsignation(models.Model):

    class Meta:
        db_table = 'request_asignation'


    apprentice = models.ForeignKey(
        Apprentice, on_delete=models.CASCADE, related_name='requests'
    )
    enterprise = models.ForeignKey(
        'assign.Enterprise', on_delete=models.CASCADE, related_name='requests'
    )
    modality_productive_stage = models.ForeignKey(
        'assign.ModalityProductiveStage', on_delete=models.CASCADE, related_name='requests'
    )
    human_talent = models.ForeignKey(
        'assign.HumanTalent', on_delete=models.CASCADE, related_name='requests', null=True, blank=True
    )
    boss = models.ForeignKey(
        'assign.Boss', on_delete=models.CASCADE, related_name='requests', null=True, blank=True
    )
    request_date = models.DateField()
    date_start_production_stage = models.DateField(null=True, blank=True)
    date_end_production_stage = models.DateField(null=True, blank=True)
    pdf_request = models.FileField(upload_to='requests/', null=True, blank=True)
    request_state = models.CharField(
        max_length=50,
        choices=RequestState.choices,
        default=RequestState.SIN_ASIGNAR
    )
    rejection_message= models.TextField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.request_state}"
