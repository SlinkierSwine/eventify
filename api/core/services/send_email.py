import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_email(email: str, subject: str, message: str) -> str:
    logger.info(f"Mail sending: to: {email}")

    email_from = settings.EMAIL_HOST_USER

    # TODO: change EmailMessage to EmailMultiAlternatives or use send_mail
    email_message = EmailMessage(
        subject=subject,
        body=message,
        from_email=email_from,
        to=[email],
        bcc=[email_from],
    )

    email_message.content_subtype = "html"

    email_message.send()

    log_msg = f"Mail has been sent to: {email}, message: {message}"
    logger.debug(log_msg)
    return log_msg
