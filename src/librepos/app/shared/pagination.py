"""Pagination utilities for LibrePOS."""

from flask import request
from flask_sqlalchemy.pagination import Pagination

DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100


def paginate_query(query, per_page: int = DEFAULT_PER_PAGE) -> Pagination:
    """Paginate a SQLAlchemy query using request args.

    Reads the 'page' parameter from the request query string and applies
    pagination to the provided query.

    Args:
        query: SQLAlchemy query object (e.g., Model.query.filter(...))
        per_page: Number of items per page (default 20, max 100)

    Returns:
        Pagination: Flask-SQLAlchemy Pagination object with attributes:
            - items: List of items for the current page
            - page: Current page number
            - pages: Total number of pages
            - total: Total number of items
            - has_prev/has_next: Boolean flags for navigation
            - prev_num/next_num: Adjacent page numbers
            - iter_pages(): Iterator for page numbers with gaps

    Example:
        pagination = paginate_query(User.query.order_by(User.name), per_page=25)
        users = pagination.items
    """
    page = request.args.get("page", 1, type=int)
    per_page = min(per_page, MAX_PER_PAGE)  # Cap at max

    return query.paginate(page=page, per_page=per_page, error_out=False)
