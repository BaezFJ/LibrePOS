from wtforms import StringField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired

from librepos.common.forms import BaseForm
from librepos.utils.form import default_placeholder


class MenuItemForm(BaseForm):
    group_id = SelectField(
        "MenuGroup",
        coerce=int,
        validators=[DataRequired()],
        render_kw=default_placeholder,
    )
    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    description = StringField("Description", render_kw=default_placeholder)
    price = FloatField(
        "Price", validators=[DataRequired()], render_kw=default_placeholder
    )
    active = BooleanField("Active", default=True)

    def __init__(self, **kwargs):
        super(MenuItemForm, self).__init__(**kwargs)
        from librepos.features.menu.repositories import MenuGroupRepository

        active_groups = MenuGroupRepository().get_active_groups()
        self.group_id.choices = [(group.id, group.name) for group in active_groups]

        if "obj" in kwargs and kwargs["obj"] is not None:
            self.price.data = float(kwargs["obj"].price) / 100
