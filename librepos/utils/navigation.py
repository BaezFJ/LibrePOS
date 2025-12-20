from urllib.parse import urlparse

from flask import request, url_for


def get_redirect_url(fallback, param_name="next"):
    """
    Get a safe redirect URL from request parameters or use a fallback.

    This function checks for a redirect parameter in the request args (default 'next'),
    validates it for security (prevents open redirects), and returns a safe URL.
    If no valid parameter is found, it returns the fallback URL.

    :param fallback: Fallback URL or endpoint name (e.g., 'main.dashboard' or '/dashboard')
    :type fallback: str
    :param param_name: Name of the query parameter to check (default: 'next')
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
    # Get the redirect URL from request parameters
    redirect_url = request.args.get(param_name)

    if redirect_url:
        # Security validation: prevent open redirects
        # Remove backslash tricks
        redirect_url = redirect_url.replace("\\", "")
        parsed_url = urlparse(redirect_url)

        # Check if it's a safe local URL (relative only, no scheme or netloc)
        if parsed_url.netloc or parsed_url.scheme or not redirect_url.startswith("/"):
            # Not safe, use fallback
            redirect_url = None

    # If no valid redirect URL, use fallback
    if not redirect_url:
        # Check if fallback looks like an endpoint (contains a dot) or a URL
        if "." in fallback and not fallback.startswith("/"):
            redirect_url = url_for(fallback)
        else:
            redirect_url = fallback

    return redirect_url
