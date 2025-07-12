from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired

from librepos.common.forms import BaseForm
from librepos.utils.form import default_placeholder, textarea_attributes


class MenuGroupForm(BaseForm):
    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()],
        render_kw=default_placeholder,
    )
    name = StringField(
        "Name", validators=[DataRequired()], render_kw=default_placeholder
    )
    description = TextAreaField("Description", render_kw=textarea_attributes)
    active = BooleanField("Active", default=True)

    def __init__(self, **kwargs):
        super(MenuGroupForm, self).__init__(**kwargs)
        from librepos.features.menu.repositories import MenuCategoryRepository

        menu_category_repository = MenuCategoryRepository()

        active_categories = menu_category_repository.get_active_categories()
        self.category_id.choices = [
            (category.id, category.name) for category in active_categories
        ]
