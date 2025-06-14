from librepos.models import RolePolicy

from . import EntityRepository


class RolePoliciesRepository(EntityRepository[RolePolicy]):
    def __init__(self):
        super().__init__(RolePolicy)

    def assign_policy_to_role(self, role_id: int, policy_id: int, assigned_by: int):
        role_policy = self.model_class(
            role_id=role_id, policy_id=policy_id, assignee_id=assigned_by
        )
        self.add(role_policy)

    def remove_policy_from_role(self, role_id: int, policy_id: int):
        policy = self.model_class.query.filter_by(
            role_id=role_id, policy_id=policy_id
        ).first()
        return self.delete(policy) if policy else None
