from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def enviar_codigo_verificacion_2fa(email, nombre, codigo, fecha_expiracion):
    """
    Envía el correo con el código de verificación 2FA para login.
    """
    html_content = render_to_string('CodigoVerificacionLogin.html', {
        'nombre': nombre,
        'codigo': codigo,
        'fecha_expiracion': fecha_expiracion
    })
    subject = 'Código de verificación para inicio de sesión SENA'
    email_msg = EmailMultiAlternatives(subject, '', to=[email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
    return True
