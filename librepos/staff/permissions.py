"""Staff blueprint permissions and policy mappings."""

from enum import StrEnum

from librepos.permissions import PolicyDefinition


class StaffPermissions(StrEnum):
    """Permissions for staff management functionality."""

    # Staff Management
    VIEW_EMPLOYEES = "view_employees"
    MANAGE_EMPLOYEES = "manage_employees"
    VIEW_TIMECLOCK = "view_timeclock"
    MANAGE_TIMECLOCK = "manage_timeclock"
    CLOCK_IN_OUT = "clock_in_out"

    # Reports
    VIEW_EMPLOYEE_REPORTS = "view_employee_reports"


# ============================================================================
# Default Policy Definitions
# ============================================================================

STAFF_FULL_ACCESS_POLICY = PolicyDefinition(
    name="Staff Full Access",
    description="Complete access to all staff management features including employee management, timeclock, and reports",
    permissions=[
        StaffPermissions.VIEW_EMPLOYEES,
        StaffPermissions.MANAGE_EMPLOYEES,
        StaffPermissions.VIEW_TIMECLOCK,
        StaffPermissions.MANAGE_TIMECLOCK,
        StaffPermissions.CLOCK_IN_OUT,
        StaffPermissions.VIEW_EMPLOYEE_REPORTS,
    ],
    is_system=True,
)

STAFF_LIMITED_ACCESS_POLICY = PolicyDefinition(
    name="Staff Limited Access",
    description="View employees and manage timeclock operations without employee management access",
    permissions=[
        StaffPermissions.VIEW_EMPLOYEES,
        StaffPermissions.VIEW_TIMECLOCK,
        StaffPermissions.MANAGE_TIMECLOCK,
        StaffPermissions.CLOCK_IN_OUT,
        StaffPermissions.VIEW_EMPLOYEE_REPORTS,
    ],
    is_system=True,
)

STAFF_READ_ONLY_POLICY = PolicyDefinition(
    name="Staff Read Only",
    description="View-only access to employee information and timeclock data",
    permissions=[
        StaffPermissions.VIEW_EMPLOYEES,
        StaffPermissions.VIEW_TIMECLOCK,
    ],
    is_system=True,
)

STAFF_SELF_SERVICE_POLICY = PolicyDefinition(
    name="Staff Self Service",
    description="Basic employee self-service for clocking in and out",
    permissions=[
        StaffPermissions.CLOCK_IN_OUT,
    ],
    is_system=True,
)

# Collection of all default policies for this blueprint
DEFAULT_POLICIES = [
    STAFF_FULL_ACCESS_POLICY,
    STAFF_LIMITED_ACCESS_POLICY,
    STAFF_READ_ONLY_POLICY,
    STAFF_SELF_SERVICE_POLICY,
]
