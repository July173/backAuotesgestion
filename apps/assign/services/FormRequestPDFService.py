from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.FormRequestPDFRepository import FormRequestRepository
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class FormRequestService(BaseService):
    def __init__(self):
        self.repository = FormRequestRepository()
    
    def upload_pdf_to_request(self, request_id, validated_data):
        try:
            logger.info(f"Iniciando carga de PDF para solicitud ID: {request_id}")
            
            pdf_file = validated_data['pdf_file']
            
            # VALIDACIONES DE NEGOCIO
            
            # Validar que el archivo no esté vacío
            if not pdf_file:
                raise ValueError("No se proporcionó ningún archivo PDF")
            
            # Validar request_id
            if not request_id or request_id <= 0:
                raise ValueError("ID de solicitud inválido")
            
            # Validar tamaño del archivo (redundante pero por seguridad)
            if pdf_file.size > 10 * 1024 * 1024:  # 10MB
                raise ValueError("El archivo PDF no puede ser mayor a 10MB")
            
            # Validar extensión (redundante pero por seguridad)
            if not pdf_file.name.lower().endswith('.pdf'):
                raise ValueError("El archivo debe ser un PDF (.pdf)")
            
            logger.info("Validaciones de negocio completadas exitosamente")
            
            # TRANSACCIÓN ATÓMICA
            with transaction.atomic():
                # Delegar al repository (solo BD)
                updated_request = self.repository.update_request_pdf(request_id, pdf_file)
                
                if not updated_request:
                    raise ValueError(f"No se pudo actualizar la solicitud con ID {request_id}. Verifique que exista.")
                
                # Construir respuesta (lógica de presentación en service)
                response = {
                    'success': True,
                    'message': 'Archivo PDF cargado exitosamente',
                    'data': {
                        'request_id': updated_request.id,
                        'pdf_name': pdf_file.name,
                        'pdf_size': pdf_file.size,
                        'pdf_content_type': pdf_file.content_type,
                        'pdf_url': updated_request.pdf_request.url if updated_request.pdf_request else None,
                        'request_state': updated_request.request_state,
                        'updated_at': updated_request.request_date
                    }
                }
                
                logger.info(f"PDF cargado exitosamente para solicitud ID: {request_id}")
                return response
                
        except ValueError as e:
            logger.error(f"Error de validación en upload_pdf_to_request: {str(e)}")
            return {
                'success': False,
                'message': str(e),
                'error_type': 'validation_error'
            }
        except Exception as e:
            logger.error(f"Error interno en upload_pdf_to_request: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno al cargar PDF: {str(e)}',
                'error_type': 'server_error'
            }
