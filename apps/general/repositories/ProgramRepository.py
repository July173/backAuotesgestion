from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Program, Ficha
from django.utils import timezone
from django.db import transaction


class ProgramRepository(BaseRepository):
    def __init__(self):
        super().__init__(Program)

    def get_fichas_by_program(self, program_id):
        """
        Retorna todas las fichas vinculadas a un programa específico, sin filtrar por estado.
        """
        return Ficha.objects.filter(program_id=program_id)
    
    def set_active_state_program_with_fichas(self, program_id, active=True):
        """
        Activa o desactiva un programa y todas sus fichas vinculadas.
        Si active=True, activa; si active=False, desactiva.
        """
        try:
            with transaction.atomic():
                program = self.model.objects.filter(pk=program_id).first()
                if not program:
                    return False

                program.active = active
                program.delete_at = None if active else timezone.now()
                program.save()

                # Actualiza todas las fichas vinculadas
                fichas = Ficha.objects.filter(program_id=program_id)
                for ficha in fichas:
                    ficha.active = active
                    ficha.delete_at = None if active else timezone.now()
                    ficha.save()

                return True
        except Exception as e:
            print(f"Error en set_active_state_program_with_fichas: {e}")
            return False
