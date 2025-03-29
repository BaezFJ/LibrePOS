from enum import StrEnum

from flask import flash


class AlertCategory(StrEnum):
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


class Messages(StrEnum):
    AUTH_LOGIN = "You have successfully logged in."
    AUTH_LOGGED_IN = "You are already logged in."
    AUTH_INACTIVE = "Your account is not active. Please contact the site administrator."
    AUTH_LOCKED = "Your account is locked. Please contact the site administrator."
    AUTH_FAILED = "Invalid credentials please try again."
    AUTH_LOGOUT = "You have successfully logged out."
    USER_PROFILE_UPDATED = "Your profile has been updated."
    FORM_SUBMISSION_ERROR = "Form submission failed."


# Define the mapping between Messages and their corresponding AlertCategory.
MESSAGE_ALERT_MAPPING = {
    Messages.AUTH_LOGIN: AlertCategory.SUCCESS,
    Messages.AUTH_LOGGED_IN: AlertCategory.INFO,
    Messages.AUTH_INACTIVE: AlertCategory.WARNING,
    Messages.AUTH_LOCKED: AlertCategory.DANGER,
    Messages.AUTH_FAILED: AlertCategory.DANGER,
    Messages.AUTH_LOGOUT: AlertCategory.SUCCESS,
    Messages.USER_PROFILE_UPDATED: AlertCategory.SUCCESS,
    Messages.FORM_SUBMISSION_ERROR: AlertCategory.DANGER,
}


def display_message(message: Messages, category: str):
    # Use provided category if given; otherwise, look it up from the mapping.
    alert_category = category or MESSAGE_ALERT_MAPPING.get(message, AlertCategory.DANGER).value
    # Determine the message text. If the passed message isn't in the mapping, use a default error message.
    message_text = message.value if message in MESSAGE_ALERT_MAPPING else "Error Generating message"
    return flash(message_text, category=alert_category)
