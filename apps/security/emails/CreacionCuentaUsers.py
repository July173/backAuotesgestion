from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger('django')   # en lugar de __name__


def send_account_created_email(email_to: str, full_name: str, temp_password: str):
    """Send account creation email with temporary password."""
    subject = "Bienvenido a Autogestión - Credenciales de Acceso"

    context = {
        'full_name': full_name,
        'email': email_to,
        'temp_password': temp_password,
    }

    # Render HTML template
    try:
        html_content = render_to_string('CreacionCuentaUsers.html', context)
    except Exception as e:
        logger.exception('Error rendering email template: %s', e)
        html_content = None

    from_email = getattr(settings, 'EMAILS_FROM_EMAIL', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)

    msg = EmailMultiAlternatives(subject, '', from_email, [email_to])
    if html_content:
        msg.attach_alternative(html_content, 'text/html')
    try:
        msg.send()
        logger.info('Account creation email sent to %s', email_to)
    except Exception as e:
        logger.exception('Failed to send account creation email to %s: %s', email_to, e)
