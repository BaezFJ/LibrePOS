from librepos.common.base_service import BaseService
from librepos.features.iam.repositories import PolicyRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.formatters import name_formatter
from librepos.utils.validators import validate_exists


class PolicyService(BaseService):
    def __init__(self):
        self.policy_repository = PolicyRepository()

    def _validate_policy_exists(self, policy_id):
        """Validate that a policy exists and return it."""
        return validate_exists(self.policy_repository, policy_id, "Policy not found.")

    def toggle_policy_status(self, policy_id):
        """Toggle a policy's active status."""

        def _toggle_operation():
            policy = self._validate_policy_exists(policy_id)
            if not policy:
                return False

            policy.active = not policy.active
            self.policy_repository.update(policy)
            status = "activated" if policy.active else "suspended"
            FlashMessageHandler.success(f"Policy {status} successfully.")
            return True

        return self._execute_with_error_handling(
            _toggle_operation, "Error toggling policy status"
        )

    def get_policy_permissions(self, policy_id):
        """Get all permissions assigned to a policy."""

        def _get_policy_permissions_operation():
            policy = self._validate_policy_exists(policy_id)
            if not policy:
                return None

            permissions = []
            for policy_permission in policy.policy_permissions:
                permission = policy_permission.permission
                permissions.append(
                    {
                        "name": name_formatter(permission.name),
                    }
                )
            return permissions

        return self._execute_with_error_handling(
            _get_policy_permissions_operation, "Error retrieving policy permissions"
        )
