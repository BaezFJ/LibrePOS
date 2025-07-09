from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder


class MenuItemForm(FlaskForm):
    group_id = SelectField(
        "Group",
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
    active = BooleanField("Active")
    submit = SubmitField("Add Item")

    def __init__(self, **kwargs):
        super(MenuItemForm, self).__init__(**kwargs)
        from librepos.features.menu.models import MenuGroup

        active_groups = (
            MenuGroup.query.filter_by(active=True).order_by(MenuGroup.name).all()
        )
        self.group_id.choices = [(group.id, group.name) for group in active_groups]

        if "obj" in kwargs and kwargs["obj"] is not None:
            self.price.data = float(kwargs["obj"].price) / 100
