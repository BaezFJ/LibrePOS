"""Query builders for IAM models.

This module contains reusable SQLAlchemy query builders that return
Query objects for flexibility (pagination, further filtering, etc.).

Naming convention:
- Functions return Query objects, not executed results
- Use descriptive names: `get_*` for single items, `list_*` or `*_query` for collections
"""

from datetime import datetime

from librepos.extensions import db

from .models import IAMRole, IAMUser, IAMUserLoginHistory, UserStatus


def latest_login_per_user_query():
    """Build query for the most recent login per user.

    Returns a SQLAlchemy query that selects only the latest login record
    for each user, ordered by login time descending.

    Returns:
        Query: SQLAlchemy query object (not executed)

    Example:
        query = latest_login_per_user_query()
        pagination = paginate_query(query, per_page=10)
        logins = query.limit(5).all()
    """
    # Subquery: get the max login_at per user
    latest_subq = (
        db.session.query(
            IAMUserLoginHistory.user_id,
            db.func.max(IAMUserLoginHistory.login_at).label("max_login_at"),
        )
        .group_by(IAMUserLoginHistory.user_id)
        .subquery()
    )

    # Join back to get full records for the latest login per user
    return IAMUserLoginHistory.query.join(
        latest_subq,
        db.and_(
            IAMUserLoginHistory.user_id == latest_subq.c.user_id,
            IAMUserLoginHistory.login_at == latest_subq.c.max_login_at,
        ),
    ).order_by(IAMUserLoginHistory.login_at.desc())


def failed_logins_query(since: datetime):
    """Query for failed login attempts since a given datetime.

    Args:
        since: Only include logins after this datetime

    Returns:
        Query: Can be used with .count() or .all()

    Example:
        yesterday = datetime.now() - timedelta(days=1)
        count = failed_logins_query(yesterday).count()
    """
    return IAMUserLoginHistory.query.filter(
        IAMUserLoginHistory.is_successful == False,  # noqa: E712
        IAMUserLoginHistory.login_at >= since,
    )


def users_count_by_role():
    """Get user count grouped by role name.

    Returns:
        list[tuple[str, int]]: List of (role_name, count) tuples

    Example:
        for role_name, count in users_count_by_role():
            print(f"{role_name}: {count}")
    """
    return (
        db.session.query(IAMRole.name, db.func.count(IAMUser.id))
        .join(IAMUser)
        .group_by(IAMRole.name)
        .all()
    )


def users_list_query(
    search: str | None = None,
    status: str | None = None,
    sort: str = "username",
):
    """Build query for users list with optional search, filter, and sort.

    Args:
        search: Search term for username/email (case-insensitive)
        status: Filter by UserStatus value
        sort: Sort field - 'username', 'role', 'last_active', 'status'

    Returns:
        Select: SQLAlchemy select statement (execute with db.session.execute())

    Example:
        query = users_list_query(search="john", status="active", sort="role")
        users = db.session.execute(query).scalars().all()
    """
    query = db.select(IAMUser)

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            db.or_(
                IAMUser.username.ilike(search_pattern),
                IAMUser.email.ilike(search_pattern),
            )
        )

    # Apply status filter
    valid_statuses = {s.value for s in UserStatus}
    if status and status in valid_statuses:
        query = query.where(IAMUser.status == status)

    # Apply sorting
    sort_options = {
        "username": IAMUser.username,
        "role": IAMRole.name,
        "last_active": IAMUser.last_login_at.desc(),
        "status": IAMUser.status,
    }

    if sort == "role":
        query = query.outerjoin(IAMRole).order_by(sort_options[sort])
    elif sort in sort_options:
        query = query.order_by(sort_options[sort])
    else:
        query = query.order_by(IAMUser.username)

    return query
