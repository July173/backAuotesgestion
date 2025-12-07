from rest_framework import serializers
from apps.assign.entity.models import VisitFollowing


class VisitFollowingUpdateSerializer(serializers.ModelSerializer):
    # state_asignation NO es campo del modelo, se maneja en el service
    state_asignation = serializers.CharField(required=False, write_only=True)
    
    class Meta:
        model = VisitFollowing
        fields = [
            'observations',
            'state_visit',
            'date_visit_made',
            'observation_state_visit',
            'state_asignation',  # write_only - no se guarda en VisitFollowing
        ]
    
    def update(self, instance, validated_data):
        # Remover state_asignation antes de guardar (no existe en el modelo)
        validated_data.pop('state_asignation', None)
        return super().update(instance, validated_data)