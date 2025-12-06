from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.VisitFollowingRepository import VisitFollowingRepository
from apps.assign.entity.serializers.VisitFollowingUpdateSerializer import VisitFollowingUpdateSerializer
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class VisitFollowingService(BaseService):
    def __init__(self):
        self.repository = VisitFollowingRepository()
    
    def partial_update_excluding(self, visit_id, data, exclude_fields=None):
        """
        Actualiza parcialmente un VisitFollowing excluyendo los campos indicados en exclude_fields.
        Retorna la instancia actualizada o None si no existe.
        """
        if exclude_fields is None:
            exclude_fields = []
        visit = self.repository.get_by_id(visit_id)
        if not visit:
            return None
        # Build payload excluding protected fields
        allowed_payload = {k: v for k, v in (data or {}).items() if k not in exclude_fields}
        # Validate with serializer to ensure proper types/limits
        serializer = VisitFollowingUpdateSerializer(instance=visit, data=allowed_payload, partial=True)
        if not serializer.is_valid():
            # raise value error with serializer errors so caller can return 400
            raise ValueError(serializer.errors)
        serializer.save()
        return serializer.instance
    
    def upload_pdf_to_visit(self, visit_id, validated_data):
        """
        Sube un archivo PDF al reporte de una visita de seguimiento.
        
        Args:
            visit_id: ID de la visita
            validated_data: Datos validados que contienen el pdf_file
            
        Returns:
            dict: Respuesta con success, message y data
        """
        try:
            logger.info(f"Iniciando carga de PDF para visita ID: {visit_id}")
            
            pdf_file = validated_data['pdf_file']
            
            # VALIDACIONES DE NEGOCIO
            
            # Validar que el archivo no esté vacío
            if not pdf_file:
                raise ValueError("No se proporcionó ningún archivo PDF")
            
            # Validar visit_id
            if not visit_id or visit_id <= 0:
                raise ValueError("ID de visita inválido")
            
            # Validar tamaño del archivo (máximo 10MB)
            if pdf_file.size > 10 * 1024 * 1024:  # 10MB
                raise ValueError("El archivo PDF no puede ser mayor a 10MB")
            
            # Validar extensión
            if not pdf_file.name.lower().endswith('.pdf'):
                raise ValueError("El archivo debe ser un PDF (.pdf)")
            
            logger.info("Validaciones de negocio completadas exitosamente")
            
            # TRANSACCIÓN ATÓMICA
            with transaction.atomic():
                # Delegar al repository (solo BD)
                updated_visit = self.repository.update_visit_pdf(visit_id, pdf_file)
                
                if not updated_visit:
                    raise ValueError(f"No se pudo actualizar la visita con ID {visit_id}. Verifique que exista.")
                
                # Construir respuesta (lógica de presentación en service)
                response = {
                    'success': True,
                    'message': 'Archivo PDF del reporte cargado exitosamente',
                    'data': {
                        'visit_id': updated_visit.id,
                        'pdf_name': pdf_file.name,
                        'pdf_size': pdf_file.size,
                        'pdf_content_type': pdf_file.content_type,
                        'pdf_url': updated_visit.pdf_report.url if updated_visit.pdf_report else None,
                        'visit_number': updated_visit.visit_number,
                        'state_visit': updated_visit.state_visit,
                        'name_visit': updated_visit.name_visit
                    }
                }
                
                logger.info(f"PDF cargado exitosamente para visita ID: {visit_id}")
                return response
                
        except ValueError as e:
            logger.error(f"Error de validación en upload_pdf_to_visit: {str(e)}")
            return {
                'success': False,
                'message': str(e),
                'error_type': 'validation_error'
            }
        except Exception as e:
            logger.error(f"Error interno en upload_pdf_to_visit: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno al cargar PDF: {str(e)}',
                'error_type': 'server_error'
            }
