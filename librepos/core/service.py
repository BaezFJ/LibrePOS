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

    def _create_entity(self, entity, repository, success_message, error_message):
        """
        Generic method to create an entity with error handling.

        Args:
            entity: The model instance to create
            repository: The repository to use for adding the entity
            success_message: Message to display on successful creation
            error_message: Message prefix to display on error

        Returns:
            The created entity on success, None on failure
        """

        def _create_operation():
            repository.add(entity)
            FlashMessageHandler.success(success_message)
            return entity

        return self._execute_with_error_handling(_create_operation, error_message)
