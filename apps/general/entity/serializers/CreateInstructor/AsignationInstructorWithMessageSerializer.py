from rest_framework import serializers
from apps.assign.entity.models import AsignationInstructor, RequestAsignation
from apps.general.entity.models import Instructor
from apps.assign.entity.enums.request_state_enum import RequestState


class AsignationInstructorWithMessageSerializer(serializers.ModelSerializer):
    programa = serializers.SerializerMethodField(read_only=True)
    messages = serializers.SerializerMethodField(read_only=True)
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    request_asignation = serializers.PrimaryKeyRelatedField(queryset=RequestAsignation.objects.all())
    request_state = serializers.ChoiceField(choices=[(choice.value, choice.label) for choice in RequestState], required=False, write_only=True)

    # Campos de solo lectura para exponer datos relacionados
    aprendiz_id = serializers.SerializerMethodField(read_only=True)
    nombre = serializers.SerializerMethodField(read_only=True)
    tipo_identificacion = serializers.SerializerMethodField(read_only=True)
    numero_identificacion = serializers.SerializerMethodField(read_only=True)
    fecha_solicitud = serializers.SerializerMethodField(read_only=True)
    estado_solicitud = serializers.SerializerMethodField(read_only=True)
    modalidad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AsignationInstructor
        fields = [
            'id',
            'instructor',
            'request_asignation',
            'request_state',
            'aprendiz_id',
            'nombre',
            'tipo_identificacion',
            'numero_identificacion',
            'fecha_solicitud',
            'estado_solicitud',
            'modalidad',
            'messages',
            'programa'
        ]
    def get_messages(self, obj):
        try:
            messages = obj.request_asignation.messages.all()
            return [
                {
                    'id': m.id,
                    'content': m.content,
                    'type_message': m.type_message,
                    'whose_message': m.whose_message
                }
                for m in messages
            ]
        except Exception:
            return []

    def get_aprendiz_id(self, obj):
        try:
            return obj.request_asignation.apprentice.id
        except Exception:
            return None

    def get_nombre(self, obj):
        try:
            person = obj.request_asignation.apprentice.person
            return f"{person.first_name} {person.first_last_name}"
        except Exception:
            return None

    def get_tipo_identificacion(self, obj):
        try:
            person = obj.request_asignation.apprentice.person
            return person.type_identification.name
        except Exception:
            return None

    def get_numero_identificacion(self, obj):
        try:
            person = obj.request_asignation.apprentice.person
            return person.number_identification
        except Exception:
            return None

    def get_modalidad(self, obj):
        try:
            mod = obj.request_asignation.modality_productive_stage
            return getattr(mod, 'name_modality', None) if mod else None
        except Exception:
            return None

    def get_fecha_solicitud(self, obj):
        try:
            return obj.request_asignation.request_date
        except Exception:
            return None

    def get_estado_solicitud(self, obj):
        try:
            return obj.request_asignation.request_state
        except Exception:
            return None

    def get_programa(self, obj):
        try:
            return obj.request_asignation.apprentice.ficha.program.name
        except Exception:
            return None