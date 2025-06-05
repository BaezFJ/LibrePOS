from typing import Optional
from flask import flash


class FlashMessageHandler:
    """Utility class for handling flash messages in the application."""

    @staticmethod
    def info(message: str, category: str = "info") -> None:
        """
        Display an info flash message.

        Args:
            message: Info message to display
            category: Message category (defaults to 'info')
        """
        flash(message, category)

    @staticmethod
    def success(message: str, category: str = "success") -> None:
        """
        Display a success flash message.
        
        Args:
            message: Success message to display
            category: Message category (defaults to 'success')
        """
        flash(message, category)

    @staticmethod
    def warning(message: str, category: str = "warning") -> None:
        """
        Display a warning flash message.
        
        Args:
            message: Warning message to display
            category: Message category (defaults to 'warning')
        """
        flash(message, category)

    @staticmethod
    def error(message: str, error: Optional[Exception] = None, category: str = "error") -> None:
        """
        Display an error flash message.
        
        Args:
            message: Base error message to display
            error: Optional exception that occurred
            category: Message category (defaults to 'error')
        """
        message = f"{message}"
        full_message = f"{message}: {str(error)}" if error else message
        flash(full_message, category)
