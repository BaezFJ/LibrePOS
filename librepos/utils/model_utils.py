from typing import Dict, Any, TypeVar

T = TypeVar("T")


def update_model_fields(model, data: Dict[str, Any]) -> None:
    """
    Update model instance fields from a dictionary of values.

    Args:
        model: Any model instance to update
        data: Dictionary containing field names and their new values
    """
    for field, value in data.items():
        if hasattr(model, field):
            setattr(model, field, value)
