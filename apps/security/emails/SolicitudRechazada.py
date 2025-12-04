from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_rejection_email(email, nombre_aprendiz, mensaje_rechazo):
	subject = 'Solicitud rechazada - SENA Sistema de Autogestión'
	from_email = 'no-reply@sena.edu.co'
	context = {
		'nombre_aprendiz': nombre_aprendiz,
		'mensaje_rechazo': mensaje_rechazo
	}
	html_content = render_to_string('SolicitudRechazada.html', context)
	msg = EmailMultiAlternatives(subject, '', from_email, [email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
