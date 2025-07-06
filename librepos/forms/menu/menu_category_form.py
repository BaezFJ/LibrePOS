from wtforms import SubmitField

from librepos.forms.base import NamedEntityForm


class MenuCategoryForm(NamedEntityForm):
    submit = SubmitField("Add Category")
