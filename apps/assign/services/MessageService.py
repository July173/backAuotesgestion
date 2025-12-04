from apps.assign.repositories.MessageRepository import MessageRepository
from apps.assign.entity.models import RequestAsignation


class MessageService:
    def __init__(self):
        self.repository = MessageRepository()

    def get(self):
        return self.repository.get()

    def get_by_id(self, pk):
        msg = self.repository.get_by_id(pk)
        if not msg:
            return {
                "status": "error",
                "type": "not_found",
                "detail": f"No existe un mensaje con id {pk}."
            }
        return msg

    def create(self, validated_data):
        # Validación simplificada de campos obligatorios
        required_fields = {
            'request_asignation': "El campo 'request_asignation' es obligatorio.",
            'content': "El campo 'content' es obligatorio.",
            'type_message': "El campo 'type_message' es obligatorio."
        }
        for field, msg in required_fields.items():
            if not validated_data.get(field):
                return {
                    "status": "error",
                    "type": "missing_data",
                    "detail": msg
                }

        request_asignation = validated_data.get('request_asignation')
        content = validated_data.get('content')
        type_message = validated_data.get('type_message')

        # Validar existencia de RequestAsignation
        if not request_asignation:
            return {
                "status": "error",
                "type": "not_found",
                "detail": f"No existe una solicitud de asignación con ese id."
            }

        message = self.repository.create(request_asignation, content, type_message)
        return message

    # Note: update_request_state removed — message/request state updates are handled elsewhere