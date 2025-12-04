from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import RequestAsignation
import logging

logger = logging.getLogger(__name__)

class FormRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(RequestAsignation)
    
    def update_request_pdf(self, request_id, pdf_file):
        try:
            logger.info(f"Actualizando PDF para solicitud ID: {request_id}")
            
            # Buscar la solicitud existente
            request_asignation = RequestAsignation.objects.get(id=request_id)
            
            # Actualizar con el PDF
            request_asignation.pdf_request = pdf_file
            request_asignation.save()
            
            logger.info(f"PDF actualizado exitosamente para solicitud ID: {request_id}")
            return request_asignation
            
        except RequestAsignation.DoesNotExist:
            logger.error(f"Solicitud con ID {request_id} no encontrada")
            return None
        except Exception as e:
            logger.error(f"Error en update_request_pdf: {e}")
            return None
