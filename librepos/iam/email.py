"""Email utilities for IAM module."""

from flask import current_app, render_template, url_for

from librepos.utils.email import send_email


def send_invitation_email(user, token: str) -> bool:
    """Send an invitation email to a newly created user.

    Args:
        user: The IAMUser instance to send the invitation to.
        token: The verification token for password setup.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    app_name = current_app.config.get("APP_NAME", "LibrePOS")
    invitation_url = url_for("iam.accept_invitation", token=token, _external=True)

    html_body = render_template(
        "iam/emails/invitation.html",
        user=user,
        invitation_url=invitation_url,
        app_name=app_name,
    )

    text_body = render_template(
        "iam/emails/invitation.txt",
        user=user,
        invitation_url=invitation_url,
        app_name=app_name,
    )

    return send_email(
        to=[user.email],
        subject=f"You're invited to join {app_name}",
        text_body=text_body,
        html_body=html_body,
    )


def send_welcome_email(user) -> bool:
    """Send a welcome email after successful account activation.

    Args:
        user: The IAMUser instance to send the welcome email to.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    app_name = current_app.config.get("APP_NAME", "LibrePOS")
    login_url = url_for("iam.login", _external=True)

    html_body = render_template(
        "iam/emails/welcome.html",
        user=user,
        login_url=login_url,
        app_name=app_name,
    )

    text_body = render_template(
        "iam/emails/welcome.txt",
        user=user,
        login_url=login_url,
        app_name=app_name,
    )

    return send_email(
        to=[user.email],
        subject=f"Welcome to {app_name}!",
        text_body=text_body,
        html_body=html_body,
    )


def send_password_reset_email(user, token: str) -> bool:
    """Send a password reset email to the user.

    Args:
        user: The IAMUser instance to send the reset email to.
        token: The verification token for password reset.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    app_name = current_app.config.get("APP_NAME", "LibrePOS")
    reset_url = url_for("iam.reset_password", token=token, _external=True)

    html_body = render_template(
        "iam/emails/password_reset.html",
        user=user,
        reset_url=reset_url,
        app_name=app_name,
    )

    text_body = render_template(
        "iam/emails/password_reset.txt",
        user=user,
        reset_url=reset_url,
        app_name=app_name,
    )

    return send_email(
        to=[user.email],
        subject=f"Reset your {app_name} password",
        text_body=text_body,
        html_body=html_body,
    )
