from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import VisitFollowing
import logging

logger = logging.getLogger(__name__)


class VisitFollowingRepository(BaseRepository):
    def __init__(self):
        super().__init__(VisitFollowing)
    
    def update_visit_pdf(self, visit_id, pdf_file):
        """
        Actualiza el campo pdf_report de una visita de seguimiento.
        
        Args:
            visit_id: ID de la visita a actualizar
            pdf_file: Archivo PDF a guardar
            
        Returns:
            VisitFollowing: Instancia actualizada o None si no existe
        """
        try:
            logger.info(f"Actualizando PDF para visita ID: {visit_id}")
            
            # Buscar la visita existente
            visit = VisitFollowing.objects.get(id=visit_id)
            
            # Actualizar con el PDF
            visit.pdf_report = pdf_file
            visit.save()
            
            logger.info(f"PDF actualizado exitosamente para visita ID: {visit_id}")
            return visit
            
        except VisitFollowing.DoesNotExist:
            logger.error(f"Visita con ID {visit_id} no encontrada")
            return None
        except Exception as e:
            logger.error(f"Error en update_visit_pdf: {e}")
            return None
