from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

from librepos.utils.form import default_placeholder


class MenuGroupForm(FlaskForm):
    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()],
        render_kw=default_placeholder,
    )
    name = StringField("Name", validators=[DataRequired()], render_kw=default_placeholder)
    active = BooleanField("Active")
    submit = SubmitField("Add Group")

    def __init__(self, **kwargs):
        super(MenuGroupForm, self).__init__(**kwargs)
        from librepos.features.menu.models import MenuCategory

        active_categories = (
            MenuCategory.query.filter_by(active=True).order_by(MenuCategory.name).all()
        )
        self.category_id.choices = [
            (category.id, category.name) for category in active_categories
        ]
