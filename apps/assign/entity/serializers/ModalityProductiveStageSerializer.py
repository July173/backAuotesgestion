from rest_framework import serializers
from apps.assign.entity.models import ModalityProductiveStage


class ModalityProductiveStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModalityProductiveStage
        fields = [
            'id',
            'name_modality',
            'description',
            'active'
        ]
