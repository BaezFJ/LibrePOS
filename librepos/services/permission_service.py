import logging
from typing import List

from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from librepos.repositories import (
    RoleRepository,
    PolicyRepository,
    RolePoliciesRepository,
)
from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields


class PermissionService:
    def __init__(self):
        self.role_repository = RoleRepository()
        self.policy_repository = PolicyRepository()
        self.role_policies_repository = RolePoliciesRepository()

    def _get_role_or_raise(self, role_id: int):
        """Helper method to get a role or raise an appropriate exception."""
        role = self.role_repository.get_by_id(role_id)
        if not role:
            FlashMessageHandler.error("Role not found.")
            raise ValueError(f"Role with ID {role_id} not found")
        return role

    def _get_active_policies_or_raise(self) -> List:
        """Helper method to get active policies or raise an appropriate exception."""
        policies = self.policy_repository.list_active_policies()
        if not policies:
            FlashMessageHandler.error("No policies found.")
            raise RuntimeError("No active policies available")
        return policies

    def list_roles(self):
        try:
            roles = self.role_repository.get_all()

            if not roles:
                FlashMessageHandler.error("No roles found.")
                return None

            return roles
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error retrieving roles: {str(e)}")
            return None

    def get_role(self, role_id: int):
        try:
            role = self.role_repository.get_by_id(role_id)

            if not role:
                FlashMessageHandler.error("Role not found.")
                return None

            return role
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error retrieving role: {str(e)}")
            return None

    def list_unassign_policies(self, role_id):
        """
        Get policies that are not assigned to the specified role.

        Args:
            role_id: The ID of the role to check

        Returns:
            List of unassigned policies

        Raises:
            ValueError: If a role is not found
            RuntimeError: If no active policies exist
            SQLAlchemyError: For database-related errors
        """
        logger = logging.getLogger(__name__)

        try:
            # Early validation with specific error messages
            role = self._get_role_or_raise(role_id)
            policies = self._get_active_policies_or_raise()

            # Use set operations for better performance with large datasets
            assigned_policy_ids = {policy.policy_id for policy in role.role_policies}
            unassigned_policies = [
                policy for policy in policies if policy.id not in assigned_policy_ids
            ]

            # Log for debugging (remove print statement)
            if unassigned_policies:
                logger.debug(
                    f"Found {len(unassigned_policies)} unassigned policies for role {role_id}: "
                    f"{[policy.name for policy in unassigned_policies]}"
                )
            else:
                logger.info(f"All policies are assigned to role {role_id}")

            return unassigned_policies

        except SQLAlchemyError as e:
            logger.error(
                f"Database error retrieving unassigned policies for role {role_id}: {str(e)}"
            )
            FlashMessageHandler.error(f"Error retrieving policies: {str(e)}")
            raise

    def assign_policies(self, role_id, policy_ids):
        try:
            role = self.role_repository.get_by_id(role_id)

            if not role:
                FlashMessageHandler.error("Role not found.")
                return None

            for policy_id in policy_ids:
                policy = self.policy_repository.get_by_id(policy_id)
                if not policy:
                    FlashMessageHandler.error("Policy not found.")
                    return None
                if policy in role.role_policies:
                    FlashMessageHandler.error("Policy already assigned to role.")
                    return None

                self.role_policies_repository.assign_policy_to_role(
                    role_id=role_id, policy_id=policy_id, assigned_by=current_user.id
                )
                FlashMessageHandler.success("Policies assigned successfully.")
                return role
            return None
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error assigning policies: {str(e)}")
            return None

    def unassign_policy(self, role_id: int, policy_id: int):
        try:
            role = self.role_repository.get_by_id(role_id)
            policy = self.policy_repository.get_by_id(policy_id)

            if not role or not policy:
                FlashMessageHandler.error("Role or policy not found.")
                return None

            if role.name == "admin" and policy.name == "administrator":
                FlashMessageHandler.error("Cannot unassign administrator policy.")
                return None

            self.role_policies_repository.remove_policy_from_role(
                role_id=role_id, policy_id=policy_id
            )
            FlashMessageHandler.success("Role policy unassigned successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error unassigning role policy: {str(e)}")
            return None

    def create_role(self, data):
        try:
            role = self.role_repository.model_class(**data)

            self.role_repository.add(role)
            FlashMessageHandler.success("Role created successfully.")
            return role
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating role: {str(e)}")
            return None

    def update_role(self, role_id, data):
        try:
            role = self.role_repository.get_by_id(role_id)

            if not role:
                FlashMessageHandler.error("Role not found.")
                return None

            # Update the fields
            update_model_fields(role, data)

            # Perform the update
            self.role_repository.update(role)
            FlashMessageHandler.success("Role updated successfully.")
            return role
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating role: {str(e)}")
            return None
