from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_assignment_to_instructor_email(email, nombre_aprendiz, nombre_instructor, numero_documento, correo_aprendiz):
    subject = 'Asignacion De Un Instructor De Seguimiento - SENA Sistema de Autogestión'
    from_email = settings.EMAILS_FROM_EMAIL if hasattr(settings, 'EMAILS_FROM_EMAIL') else 'no-reply@sena.edu.co'
    context = {
        'nombre_aprendiz': nombre_aprendiz,
        'nombre_instructor': nombre_instructor,
        'numero_documento': numero_documento,
        'correo_aprendiz': correo_aprendiz
    }
    html_content = render_to_string('AsignacionInstructor.html', context)
    msg = EmailMultiAlternatives(subject, '', from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_instructor_assignment_email(email, nombre_aprendiz, nombre_instructor, numero_documento, correo_aprendiz):
    subject = 'Nueva Asignación de Seguimiento - SENA Sistema de Autogestión'
    from_email = settings.EMAILS_FROM_EMAIL if hasattr(settings, 'EMAILS_FROM_EMAIL') else 'no-reply@sena.edu.co'
    context = {
        'nombre_aprendiz': nombre_aprendiz,
        'nombre_instructor': nombre_instructor,
        'numero_documento': numero_documento,
        'correo_aprendiz': correo_aprendiz
    }
    # Este correo se envía al aprendiz; usar plantilla diseñada para el aprendiz
    html_content = render_to_string('AsignacionInstructorParaInstructor.html', context)
    msg = EmailMultiAlternatives(subject, '', from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
