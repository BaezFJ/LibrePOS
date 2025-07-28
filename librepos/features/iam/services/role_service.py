from flask_login import current_user

from librepos.common.base_service import BaseService
from librepos.utils import FlashMessageHandler
from librepos.utils.formatters import name_formatter
from librepos.utils.validators import validate_exists, validate_confirmation
from ..repositories import RoleRepository, PolicyRepository, RolePolicyRepository


class RoleService(BaseService):
    def __init__(self):
        self.role_repository = RoleRepository()
        self.policy_repository = PolicyRepository()
        self.role_policies_repository = RolePolicyRepository()

    def _validate_role_exists(self, role_id):
        """Validate that a role exists and return it."""
        return validate_exists(self.role_repository, role_id, "Role not found.")

    def _validate_policy_exists(self, policy_id):
        """Validate that a policy exists and return it."""
        return validate_exists(self.policy_repository, policy_id, "Policy not found.")

    def _validate_role_and_policy(self, role_id, policy_id):
        """Validate that both role and policy exist and return them."""
        role = self._validate_role_exists(role_id)
        policy = self._validate_policy_exists(policy_id)
        return role, policy

    def create_role(self, data):
        """Create a new role."""

        def _create_operation():
            role = self.role_repository.model_class(**data)
            self.role_repository.add(role)
            FlashMessageHandler.success("Role created successfully.")
            return role

        return self._execute_with_error_handling(
            _create_operation, "Error creating role"
        )

    def delete_role(self, data, role_id):
        """Delete a role."""

        def _delete_operation():
            role = self._validate_role_exists(role_id)
            if not role:
                return False

            if not validate_confirmation(data):
                return False

            self.role_repository.delete(role)
            FlashMessageHandler.success("Role deleted successfully.")
            return True

        return self._execute_with_error_handling(
            _delete_operation, "Error deleting role"
        )

    def toggle_role_status(self, role_id):
        """Toggle a role's active status."""

        def _toggle_operation():
            role = self._validate_role_exists(role_id)
            if not role:
                return False

            role.active = not role.active
            self.role_repository.update(role)
            status = "activated" if role.active else "suspended"
            FlashMessageHandler.success(f"Role {status} successfully.")
            return True

        return self._execute_with_error_handling(
            _toggle_operation, "Error toggling role status"
        )

    def get_unassigned_policies(self, role_id):
        """Get policies that are not assigned to a role."""

        def _get_unassigned_operation():
            role = self._validate_role_exists(role_id)
            if not role:
                return None

            policies = self.policy_repository.get_all()
            if not policies:
                FlashMessageHandler.error("No policies found.")
                return None

            assigned_policy_ids = {
                role_policy.policy_id for role_policy in role.role_policies
            }
            return [
                policy for policy in policies if policy.id not in assigned_policy_ids
            ]

        return self._execute_with_error_handling(
            _get_unassigned_operation, "Error retrieving unassigned policies"
        )

    def assign_policy_to_role(self, role_id, policy_id):
        """Assign a policy to a role."""

        def _assign_operation():
            role, policy = self._validate_role_and_policy(role_id, policy_id)
            if not role or not policy:
                return None

            if policy in role.role_policies:
                FlashMessageHandler.error("Policy already assigned to role.")
                return None

            assigned_role_policy = self.role_policies_repository.model_class(
                role_id=role_id, policy_id=policy_id, assignee_id=current_user.id
            )
            self.role_policies_repository.add(assigned_role_policy)

            policy_name = name_formatter(policy.name)
            FlashMessageHandler.success(f"Policy {policy_name} assigned successfully.")
            return assigned_role_policy

        return self._execute_with_error_handling(
            _assign_operation, "Error assigning policy"
        )

    def remove_policy_from_role(self, role_id, policy_id):
        """Remove a policy from a role."""

        def _remove_operation():
            role, policy = self._validate_role_and_policy(role_id, policy_id)
            if not role or not policy:
                return None

            self.role_policies_repository.remove_policy_from_role(
                role_id=role_id, policy_id=policy_id
            )

            policy_name = name_formatter(policy.name)
            FlashMessageHandler.success(f"Policy {policy_name} removed successfully.")
            return True

        return self._execute_with_error_handling(
            _remove_operation, "Error removing policy"
        )
