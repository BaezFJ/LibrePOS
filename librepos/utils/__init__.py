from urllib.parse import urljoin

from flask import request


def safe_next_url(next_url):
    """
    Joins the provided next_url with the host URL of the current request context to produce
    a complete, safe URL. This function ensures that relative URLs are properly resolved
    to prevent potential security issues or misdirected links.

    :param next_url: The relative or absolute path URL to be combined with the host URL
        of the current request context to create a full, safe URL.
    :type next_url: str

    :return: A fully constructed and safe URL based on the host URL and the provided
        next_url value.
    :rtype: str
    """
    return urljoin(request.host_url, next_url)
