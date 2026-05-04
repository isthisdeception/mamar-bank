import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_html_email(subject, template, context, to_email):
    """
    Send HTML mail. Does not raise: SMTP errors are logged so the HTTP request
    still completes after a successful transaction.
    """
    if not to_email:
        logger.warning("send_html_email skipped: empty recipient (subject=%r)", subject)
        return

    try:
        html_content = render_to_string(template, context)
        email = EmailMultiAlternatives(
            subject=subject,
            body="Fallback text",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception:
        logger.exception(
            "send_html_email failed subject=%r to=%r host=%r",
            subject,
            to_email,
            getattr(settings, "EMAIL_HOST", "") or "(console)",
        )