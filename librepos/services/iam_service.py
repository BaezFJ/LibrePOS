from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from librepos.repositories import (
    UserRepository,
    RoleRepository,
    PolicyRepository,
    RolePoliciesRepository,
)
from librepos.utils import FlashMessageHandler
from librepos.utils.formatters import un_snake_formatter, strip_spaces_formatter
from librepos.utils.model_utils import update_model_fields


class IAMService:
    """Service for Identity and Access Management (IAM) operations."""

    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()
        self.policy_repository = PolicyRepository()
        self.role_policies_repository = RolePoliciesRepository()

    # ==================================================================================================================
    #                                              USERS
    # ==================================================================================================================

    def create_user(self, data):
        """Create a new user."""
        try:
            user = self.user_repository.model_class(**data)

            self.user_repository.add(user)
            FlashMessageHandler.success("User created successfully.")
            return user

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating user: {str(e)}")
            return None

    def delete_user(self, data):
        """Delete a user."""
        try:
            user = self.user_repository.get_by_id(data.get("id"))
            confirmation = data.get("confirmation").lower()

            if not user:
                FlashMessageHandler.error("User not found.")
                return False

            if confirmation != "confirm":
                FlashMessageHandler.error("Invalid confirmation.")
                return False

            self.user_repository.delete(user)
            FlashMessageHandler.success("User deleted successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error deleting user: {str(e)}")
            return False

    def toggle_user_status(self, user_id):
        """Toggle a user's active status."""
        try:
            user = self.user_repository.get_by_id(user_id)

            if not user:
                FlashMessageHandler.error("User not found.")
                return False

            user.active = not user.active
            self.user_repository.update(user)
            status = "activated" if user.active else "suspended"
            FlashMessageHandler.success(f"User {status} successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error toggling user status: {str(e)}")
            return False

    def update_user(self, user_id, data):
        """Update a user."""
        try:
            user = self.user_repository.get_by_id(user_id)

            if not user:
                FlashMessageHandler.error("User not found.")
                return False

            update_model_fields(user, data)
            self.user_repository.update(user)
            FlashMessageHandler.success("User updated successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating user: {str(e)}")

    # ==================================================================================================================
    #                                              ROLES
    # ==================================================================================================================

    def create_role(self, data):
        """Create a new role."""
        try:
            role = self.role_repository.model_class(**data)

            self.role_repository.add(role)
            FlashMessageHandler.success("Role created successfully.")
            return role
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating role: {str(e)}")
            return None

    def delete_role(self, data, role_id):
        """Delete a role."""
        try:
            role = self.role_repository.get_by_id(role_id)
            confirmation = data.get("confirmation").lower()

            if not role:
                FlashMessageHandler.error("Role not found.")
                return False

            if confirmation != "confirm":
                FlashMessageHandler.error("Invalid confirmation.")
                return False
            self.role_repository.delete(role)
            FlashMessageHandler.success("Role deleted successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error deleting role: {str(e)}")
            return False

    def toggle_role_status(self, role_id):
        """Toggle a role's active status."""
        try:
            role = self.role_repository.get_by_id(role_id)

            if not role:
                FlashMessageHandler.error("Role not found.")
                return False

            role.active = not role.active
            self.role_repository.update(role)
            status = "activated" if role.active else "suspended"
            FlashMessageHandler.success(f"Role {status} successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error toggling role status: {str(e)}")
            return False

    # ==================================================================================================================
    #                                              ROLES POLICIES
    # ==================================================================================================================

    def get_unassigned_policies(self, role_id):
        """Get policies that are not assigned to a role."""
        try:
            role = self.role_repository.get_by_id(role_id)
            policies = self.policy_repository.list_active_policies()

            if not role:
                FlashMessageHandler.error("Role not found.")
                return None

            if not policies:
                FlashMessageHandler.error("No policies found.")
                return None

            assigned_policy_ids = {
                role_policy.policy_id for role_policy in role.role_policies
            }
            unassigned_policies = [
                policy for policy in policies if policy.id not in assigned_policy_ids
            ]

            return unassigned_policies
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error retrieving unassigned policies: {str(e)}")
            return None

    def assign_policy_to_role(self, role_id, policy_id):
        """Assign a policy to a role."""
        try:
            role = self.role_repository.get_by_id(role_id)
            policy = self.policy_repository.get_by_id(policy_id)
            assigned_by = current_user.id

            if not role:
                FlashMessageHandler.error("Role not found.")
                return None

            if not policy:
                FlashMessageHandler.error("Policy not found.")
                return None

            if policy in role.role_policies:
                FlashMessageHandler.error("Policy already assigned to role.")
                return None
            assigned_role_policy = self.role_policies_repository.model_class(
                role_id=role_id, policy_id=policy_id, assignee_id=assigned_by
            )
            self.role_policies_repository.add(assigned_role_policy)
            policy_name = strip_spaces_formatter(
                un_snake_formatter(policy.name).title()
            )
            FlashMessageHandler.success(f"Policy {policy_name} assigned successfully.")
            return assigned_role_policy
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error assigning policy: {str(e)}")
            return None

    def remove_policy_from_role(self, role_id, policy_id):
        """Remove a policy from a role."""
        try:
            role = self.role_repository.get_by_id(role_id)
            policy = self.policy_repository.get_by_id(policy_id)

            if not role:
                FlashMessageHandler.error("Role not found.")
                return None

            if not policy:
                FlashMessageHandler.error("Policy not found.")
                return None

            self.role_policies_repository.remove_policy_from_role(
                role_id=role_id, policy_id=policy_id
            )
            policy_name = strip_spaces_formatter(
                un_snake_formatter(policy.name).title()
            )
            FlashMessageHandler.success(f"Policy {policy_name} removed successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error removing policy: {str(e)}")

    # ==================================================================================================================
    #                                              POLICIES
    # ==================================================================================================================

    def toggle_policy_status(self, policy_id):
        """Toggle a policy's active status."""
        try:
            policy = self.policy_repository.get_by_id(policy_id)

            if not policy:
                FlashMessageHandler.error("Policy not found.")
                return False

            policy.active = not policy.active
            self.policy_repository.update(policy)
            status = "activated" if policy.active else "suspended"
            FlashMessageHandler.success(f"Policy {status} successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error toggling policy status: {str(e)}")
