import enum

from flask import flash


class AlertCategory(enum.Enum):
    SUCCESS: str = "success"
    INFO: str = "info"
    WARNING: str = "warning"
    DANGER: str = "danger"


class Messages(enum.Enum):
    AUTH_LOGIN: str = "You have successfully logged in."
    AUTH_LOGGED_IN: str = "You are already logged in."
    AUTH_INACTIVE: str = "Your account is not active. Please contact the site administrator."
    AUTH_LOCKED: str = "Your account is locked. Please contact the site administrator."
    AUTH_FAILED: str = "Invalid credentials please try again."
    AUTH_LOGOUT: str = "You have successfully logged out."
    USER_PROFILE_UPDATED: str = "Your profile has been updated."
    FORM_SUBMISSION_ERROR: str = "Form submission failed."


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


def display_message(message: Messages, category: str = None):
    # Use provided category if given; otherwise, look it up from the mapping.
    alert_category = category or MESSAGE_ALERT_MAPPING.get(message, AlertCategory.DANGER).value
    # Determine the message text. If the passed message isn't in the mapping, use a default error message.
    message_text = message.value if message in MESSAGE_ALERT_MAPPING else "Error Generating message"
    return flash(message_text, category=alert_category)
