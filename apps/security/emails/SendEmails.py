from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def enviar_registro_pendiente(email_destino, nombre, fecha_registro):
    asunto = "Registro Exitoso - Cuenta Pendiente de Activación"
    # Renderiza el HTML usando la plantilla y los datos
    html_content = render_to_string(
        'RegistroPendiente.html',
        {
            'nombre': nombre,
            'email': email_destino,
            'fecha_registro': fecha_registro,
        }
    )
    msg = EmailMultiAlternatives(
        asunto,
        '',
        settings.EMAILS_FROM_EMAIL,
        [email_destino]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Puedes crear funciones similares para otros correos
