from rest_framework import serializers
from apps.assign.entity.models.Message import Message
from apps.assign.entity.serializers.form.RequestAsignationSerializer import RequestAsignationSerializer


class ChangeInAsignationSerializer(serializers.ModelSerializer):
	content = serializers.CharField(required=False)
	type_message = serializers.CharField(required=False)
	whose_message = serializers.CharField(required=False, allow_null=True, allow_blank=True)
	request_state = serializers.CharField(required=False)
	fecha_inicio_contrato = serializers.DateField(required=False, allow_null=True)
	fecha_fin_contrato = serializers.DateField(required=False, allow_null=True)

	class Meta:
		model = Message
		fields = [
			'id',
			'content',
			'type_message',
			'whose_message',
			'fecha_inicio_contrato',
			'fecha_fin_contrato',
			'request_state'
		]

	def get_fecha_inicio_contrato(self, obj):
		try:
			return obj.request_asignation.date_start_production_stage
		except Exception:
			return None

	def get_fecha_fin_contrato(self, obj):
		try:
			return getattr(obj.request_asignation, 'date_end_production_stage', None)
		except Exception:
			return None
    