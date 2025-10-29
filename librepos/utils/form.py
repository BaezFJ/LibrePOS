def sanitize_form_data(form, exclude_fields: list[str] | None = None):
    """
    Sanitizes form data by removing specified fields, including default fields such as
    CSRF token and submit button. This function is used to clean up unnecessary form data
    before further processing or saving.

    :param form: A form object that contains the data to be sanitized.
    :type form: Any
    :param exclude_fields: Optional list of field names to be excluded from the sanitized data.
    :type exclude_fields: list[str] | None
    :return: A dictionary with the sanitized form data, excluding the specified fields.
    :rtype: dict
    """
    sanitized_data = form.data

    sanitized_data.pop("csrf_token", None)
    sanitized_data.pop("submit", None)

    if exclude_fields:
        for field in exclude_fields:
            sanitized_data.pop(field, None)

    return sanitized_data
