from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    active = BooleanField("Active", default=True)


class GroupForm(FlaskForm):
    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    active = BooleanField("Active", default=True)

    def __init__(self, **kwargs):
        super(GroupForm, self).__init__(**kwargs)
        from librepos.models.menu_categories import MenuCategory

        active_categories = (
            MenuCategory.query.filter_by(active=True).order_by(MenuCategory.name).all()
        )
        self.category_id.choices = [
            (category.id, category.name) for category in active_categories
        ]


class MenuItemForm(FlaskForm):
    group_id = SelectField(
        "Group",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    description = StringField("Description", render_kw={"placeholder": " "})
    price = FloatField(
        "Price", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    active = BooleanField("Active", default=True)

    def __init__(self, **kwargs):
        super(MenuItemForm, self).__init__(**kwargs)
        from librepos.models.menu_groups import MenuGroup

        active_groups = (
            MenuGroup.query.filter_by(active=True).order_by(MenuGroup.name).all()
        )
        self.group_id.choices = [(group.id, group.name) for group in active_groups]

        if "obj" in kwargs and kwargs["obj"] is not None:
            self.price.data = float(kwargs["obj"].price) / 100
