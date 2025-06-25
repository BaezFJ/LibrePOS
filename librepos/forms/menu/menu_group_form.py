from wtforms import SelectField
from wtforms.validators import DataRequired

from librepos.forms.base import NamedEntityForm


class MenuGroupForm(NamedEntityForm):
    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )

    def __init__(self, **kwargs):
        super(MenuGroupForm, self).__init__(**kwargs)
        from librepos.models.menu_categories import MenuCategory

        active_categories = (
            MenuCategory.query.filter_by(active=True).order_by(MenuCategory.name).all()
        )
        self.category_id.choices = [
            (category.id, category.name) for category in active_categories
        ]
