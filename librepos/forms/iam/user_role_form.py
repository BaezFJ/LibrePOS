from wtforms import SelectField
from wtforms.validators import DataRequired

from librepos.forms.base import BaseForm


class UserRoleForm(BaseForm):
    role_id = SelectField(
        "Role",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )

    def __init__(self, **kwargs):
        super(UserRoleForm, self).__init__(**kwargs)

        from librepos.repositories.role_repo import RoleRepository

        self.role_id.choices = [
            (role.id, role.name.replace("_", " ").title())
            for role in RoleRepository().get_active_roles()
        ]
