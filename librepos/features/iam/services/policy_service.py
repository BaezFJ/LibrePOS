from sqlalchemy.exc import SQLAlchemyError

from librepos.features.iam.repositories import PolicyRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.formatters import strip_spaces_formatter


class PolicyService:
    def __init__(self):
        self.policy_repository = PolicyRepository()

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

    def get_policy_permissions(self, policy_id):
        """Get all permissions assigned to a policy."""
        try:
            policy = self.policy_repository.get_by_id(policy_id)

            if not policy:
                FlashMessageHandler.error("Policy not found.")
                return None

            permissions = []
            for policy_permission in policy.policy_permissions:
                permission = policy_permission.permission
                permissions.append(
                    {
                        "name": strip_spaces_formatter(
                            permission.name.replace(".", " ").title()
                        ),
                        "description": permission.description,
                    }
                )
            return permissions

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error retrieving policy permissions: {str(e)}")
            return None
