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
    resolved_to_email = to_email or getattr(settings, "EMAIL_FALLBACK_RECIPIENT", "")
    if not resolved_to_email:
        logger.warning(
            "send_html_email skipped: empty recipient and no EMAIL_FALLBACK_RECIPIENT (subject=%r)",
            subject,
        )
        return

    try:
        html_content = render_to_string(template, context)
        logger.info(
            "send_html_email: sending subject=%r to=%r backend=%s host=%r from=%r",
            subject,
            resolved_to_email,
            settings.EMAIL_BACKEND,
            getattr(settings, "EMAIL_HOST", "") or "(none — console backend prints to logs)",
            settings.DEFAULT_FROM_EMAIL,
        )
        email = EmailMultiAlternatives(
            subject=subject,
            body="Fallback text",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[resolved_to_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        logger.info(
            "send_html_email: SMTP/backend accepted message subject=%r to=%r "
            "(check inbox and spam; console backend shows full message above in logs)",
            subject,
            resolved_to_email,
        )
    except Exception:
        logger.exception(
            "send_html_email failed subject=%r to=%r host=%r",
            subject,
            resolved_to_email,
            getattr(settings, "EMAIL_HOST", "") or "(console)",
        )