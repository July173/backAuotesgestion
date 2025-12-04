from rest_framework import serializers
from apps.assign.entity.models import RequestAsignation, Enterprise, ModalityProductiveStage
from apps.general.entity.models import Apprentice

class RequestAsignationSerializer(serializers.ModelSerializer):
    apprentice = serializers.PrimaryKeyRelatedField(queryset=Apprentice.objects.all())
    enterprise = serializers.PrimaryKeyRelatedField(queryset=Enterprise.objects.all())
    modality_productive_stage = serializers.PrimaryKeyRelatedField(queryset=ModalityProductiveStage.objects.all())

    class Meta:
        model = RequestAsignation
        fields = [
            'id',
            'apprentice',
            'enterprise',
            'modality_productive_stage',
            'request_date',
            'date_start_production_stage',
            'pdf_request',
            'request_state'
        ]
