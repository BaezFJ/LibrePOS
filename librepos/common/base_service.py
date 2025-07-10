from sqlalchemy.exc import SQLAlchemyError

from librepos.utils import FlashMessageHandler


class BaseService:
    """Base service class with common database operation handling."""

    @staticmethod
    def _execute_with_error_handling(operation, error_message_prefix):
        """Handle database operations with consistent error handling."""
        try:
            return operation()
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"{error_message_prefix}: {str(e)}")
            return None
