from wtforms import StringField, FloatField, SelectField
from wtforms.validators import DataRequired

from librepos.forms.base import NamedEntityForm


class MenuItemForm(NamedEntityForm):
    group_id = SelectField(
        "Group",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )
    description = StringField("Description", render_kw={"placeholder": " "})
    price = FloatField(
        "Price", validators=[DataRequired()], render_kw={"placeholder": " "}
    )

    def __init__(self, **kwargs):
        super(MenuItemForm, self).__init__(**kwargs)
        from librepos.models.menu_groups import MenuGroup

        active_groups = (
            MenuGroup.query.filter_by(active=True).order_by(MenuGroup.name).all()
        )
        self.group_id.choices = [(group.id, group.name) for group in active_groups]

        if "obj" in kwargs and kwargs["obj"] is not None:
            self.price.data = float(kwargs["obj"].price) / 100
