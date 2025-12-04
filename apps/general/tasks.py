from celery import shared_task
from django.utils import timezone
from apps.general.entity.models import Instructor
from apps.general.repositories.InstructorRepository import InstructorRepository

@shared_task
def deactivate_expired_instructors():
    """
    Desactiva instructores cuyo contrato ha terminado (contractEndDate <= hoy).
    """
    today = timezone.now().date()
    expired_instructors = Instructor.objects.filter(contractEndDate__lte=today, active=True)
    repo = InstructorRepository()
    for instructor in expired_instructors:
        repo.set_active_state_dates_instructor(instructor, active=False)
    return f"Instructores desactivados: {expired_instructors.count()}"
