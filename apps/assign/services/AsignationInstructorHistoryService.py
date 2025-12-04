from apps.assign.repositories.AsignationInstructorHistoryRepository import AsignationInstructorHistoryRepository
from apps.assign.entity.models import AsignationInstructor
from apps.general.entity.models import Instructor
from apps.security.entity.models import User
from apps.assign.emails.DesvinculacionInstructor import send_unassignment_to_instructor_email
from apps.assign.emails.ReasignacionInstructor import send_assignment_to_new_instructor_email
from apps.assign.emails.DesvinculacionAprendiz import send_unassignment_to_aprendiz_email
from apps.general.services.NotificationService import NotificationService


class AsignationInstructorHistoryService:
    def __init__(self):
        self.repository = AsignationInstructorHistoryRepository()

    def error_response(self, message, error_type="error"):
        return {"status": "error", "type": error_type, "message": str(message)}

    def list_by_asignation(self, asignation_instructor_id):
        try:
            return self.repository.list_by_asignation(asignation_instructor_id)
        except Exception as e:
            return self.error_response(f"No se pudo obtener el historial: {e}", "list_by_asignation")

    def reasignar_instructor(self, asignation_instructor_id, new_instructor_id, message):
        try:
            asignation_instructor = AsignationInstructor.objects.get(id=asignation_instructor_id)
            old_instructor = asignation_instructor.instructor
            old_instructor_id = old_instructor.id
            new_instructor = Instructor.objects.get(id=new_instructor_id)
            # Guardar historial antes de actualizar
            self.repository.create_history(
                asignation_instructor=asignation_instructor,
                old_instructor_id=old_instructor_id,
                message=message
            )
            # Enviar correo al instructor anterior
            old_person = old_instructor.person
            old_user = User.objects.filter(person=old_person).first()
            old_email = old_user.email if old_user else None
            nombre_instructor = f"{old_person.first_name} {old_person.first_last_name}"
            aprendiz_person = asignation_instructor.request_asignation.apprentice.person
            nombre_aprendiz = f"{aprendiz_person.first_name} {aprendiz_person.first_last_name}"
            if old_email:
                send_unassignment_to_instructor_email(old_email, nombre_instructor, nombre_aprendiz)
                # Decrementar aprendices asignados al instructor anterior (atómico)
                from apps.general.services.InstructorService import InstructorService
                try:
                    InstructorService().decrement_assigned_learners(old_instructor_id, delta=1)
                except Exception as e:
                    # No detener el flujo si falla la actualización de contador
                    print(f"[AsignationInstructorHistoryService] No se pudo decrementar contador de instructor anterior: {e}")
            # Enviar correo al instructor nuevo
            new_person = new_instructor.person
            new_user = User.objects.filter(person=new_person).first()
            new_email = new_user.email if new_user else None
            new_instructor_name = f"{new_person.first_name} {new_person.first_last_name}"
            if new_email:
                send_assignment_to_new_instructor_email(new_email, new_instructor_name, nombre_aprendiz)
                # Incrementar aprendices asignados al nuevo instructor (atómico)
                from apps.general.services.InstructorService import InstructorService
                try:
                    InstructorService().increment_assigned_learners(new_instructor_id, delta=1)
                except Exception as e:
                    print(f"[AsignationInstructorHistoryService] No se pudo incrementar contador de nuevo instructor: {e}")
            # Enviar correo al aprendiz
            aprendiz_user = User.objects.filter(person=aprendiz_person).first()
            aprendiz_email = aprendiz_user.email if aprendiz_user else None
            if aprendiz_email:
                send_unassignment_to_aprendiz_email(aprendiz_email, nombre_aprendiz)
            # Notificación interna por sistema (aprendiz, instructor anterior y nuevo instructor)
            try:
                aprendiz = asignation_instructor.request_asignation.apprentice
                ficha = getattr(asignation_instructor.request_asignation, 'ficha', None)
                NotificationService().notify_reassignment(
                    apprentice=aprendiz,
                    instructor_old=old_instructor,
                    instructor_new=new_instructor,
                    ficha=ficha
                )
            except Exception as e:
                print(f"[AsignationInstructorHistoryService] No se pudo notificar la reasignación: {str(e)}")

            # Actualizar asignación con el nuevo instructor
            asignation_instructor.instructor = new_instructor
            asignation_instructor.save()
            return asignation_instructor
        except AsignationInstructor.DoesNotExist:
            return self.error_response("La asignación de instructor no existe.", "not_found")
        except Instructor.DoesNotExist:
            return self.error_response("El nuevo instructor no existe.", "not_found")
        except Exception as e:
            return self.error_response(f"Error al reasignar instructor: {e}", "reasignar_instructor")
