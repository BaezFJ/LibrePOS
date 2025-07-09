from sqlalchemy.exc import SQLAlchemyError

from librepos.utils import FlashMessageHandler


class BaseService:
    """Base service class with common database operation handling."""

    @staticmethod
    def _handle_database_operation(operation, error_message_prefix):
        """Handle database operations with consistent error handling."""
        try:
            return operation()
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"{error_message_prefix}: {str(e)}")
            return None

    @staticmethod
    def validate_exists(repository, entity_id, message):
        """Validate that an entity exists and return it."""
        entity = repository.get_by_id(entity_id)
        if not entity:
            FlashMessageHandler.error(f"{message}")
        return entity
