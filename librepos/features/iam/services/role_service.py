from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from librepos.features.iam.repositories import RoleRepository, PolicyRepository, RolePolicyRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.formatters import un_snake_formatter, strip_spaces_formatter


class RoleService:

    def __init__(self):
        self.role_repository = RoleRepository()
        self.policy_repository = PolicyRepository()
        self.role_policies_repository = RolePolicyRepository()

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
