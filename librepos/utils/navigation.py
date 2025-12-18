from urllib.parse import urlparse

from flask import request, url_for

# Define endpoints allowed for redirection
ALLOWED_REDIRECT_ENDPOINTS = {
    "main.dashboard",
    "auth.login",
    "staff.members",
    # add other allowed endpoints here if needed
}

def get_redirect_url(fallback, param_name="next", allowed_endpoints=None):
    """
    Get a safe redirect URL from request parameters or use a fallback.

    This function checks for a redirect parameter in the request args (default 'next'),
    validates it for security (prevents open redirects), and returns a safe URL.
    If no valid parameter is found, it returns the fallback URL.

    :param fallback: Fallback URL or endpoint name (e.g., 'main.dashboard')
    :type fallback: str
    :param param_name: Name of the query parameter to check (default: 'next')
    :param allowed_endpoints: Set, list, or tuple of allowed endpoint names. Defaults to ALLOWED_REDIRECT_ENDPOINTS.
    :type allowed_endpoints: set or None
    :type param_name: str
    :return: Safe URL string
    :rtype: str

    Usage in views:
        # Redirect after form submission
        return redirect(get_redirect_url('main.dashboard'))

        # Get back URL with custom parameter name
        back_url = get_redirect_url('staff.members', param_name='back')

    Usage in templates:
        context = {
            "back_url": get_redirect_url('staff.members', param_name='back')
        }
    """
    if allowed_endpoints is None:
        allowed_endpoints = ALLOWED_REDIRECT_ENDPOINTS
    # Get the redirect target from request parameters
    target = request.args.get(param_name)

    # If the user supplied a target, validate it
    if target:
        # Remove backslash tricks
        target = target.replace("\\", "")
        parsed_url = urlparse(target)
        # Allow only endpoint names in whitelist, not raw relative paths
        # E.g., if ?back=main.dashboard, allow; if ?back=/admin, disallow
        if target in allowed_endpoints:
            return url_for(target)
        # Optionally allow raw paths which exactly match those from url_for
        # else, for defense in depth, restrict to endpoints only

    # If no valid target, fall back to fallback
    if "." in fallback and not fallback.startswith("/"):
        return url_for(fallback)
    else:
        return fallback
