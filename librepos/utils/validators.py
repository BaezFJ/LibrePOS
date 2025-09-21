from librepos.utils import FlashMessageHandler


def validate_exists(repository, entity_id, message="Entity not found."):
    """Validate that an entity exists in the repository and return it.

    Args:
        repository: Repository object with get_by_id method to retrieve entities.
        entity_id: ID of the entity to validate.
        message (str, optional): Error message to display if the entity is not found
            Defaults to "Entity not found."

    Returns:
        The entity if it exists, None otherwise.
        If an entity is not found, displays an error message via FlashMessageHandler.

    Example:
        user = validate_exists(user_repository, 123, "User not found.")
        if user:
            # Process existing user
        else:
            # Handle a missing user case
    """
    entity = repository.get_by_id(entity_id)
    if not entity:
        FlashMessageHandler.error(f"{message}")
    return entity


def validate_confirmation(
    data,
    confirmation_field="confirmation",
    expected_value="confirm",
    error_message="Invalid confirmation.",
):
    """Validate confirmation input matches the expected value.

    Args:
        data (dict): Dictionary containing the confirmation input.
        confirmation_field (str, optional): Key in data dictionary for confirmation value.
            Defaults to "confirmation".
        expected_value (str, optional): Expected value for confirmation.
            Defaults to "confirm".
        error_message (str, optional): Error message to display if validation fails.
            Defaults to "Invalid confirmation."

    Returns:
        bool: True if confirmation matches the expected value, False otherwise.
            If validation fails, an error message is displayed via FlashMessageHandler.
    """
    confirmation = data.get(confirmation_field, "").lower()
    if confirmation != expected_value:
        FlashMessageHandler.error(error_message)
        return False
    return True
