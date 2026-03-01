"""Email utilities for LibrePOS."""

from flask import current_app
from flask_mailman import EmailMultiAlternatives


def send_email(
    to: list[str],
    subject: str,
    text_body: str,
    html_body: str | None = None,
) -> bool:
    """Send an email using Flask-Mailman.

    Args:
        to: List of recipient email addresses.
        subject: Email subject line.
        text_body: Plain text email body.
        html_body: Optional HTML email body.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    try:
        msg = EmailMultiAlternatives(subject=subject, body=text_body, to=to)
        if html_body:
            msg.attach_alternative(html_body, "text/html")
        msg.send()
        return True
    except Exception as e:
        current_app.logger.error(f"Email send failed: {e}")
        return False
