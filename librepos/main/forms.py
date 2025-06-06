from babel.numbers import list_currencies
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import DataRequired

from librepos.utils.datetime import get_all_timezones


class RestaurantForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    address = StringField(
        "Address", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    city = StringField(
        "City", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    state = StringField(
        "State", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    zipcode = StringField(
        "Zipcode", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    country = StringField(
        "Country", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    phone = StringField(
        "Phone", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    email = StringField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": " "}
    )
    website = StringField("Website", render_kw={"placeholder": " "})
    currency = SelectField(
        "Currency",
        coerce=str,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )
    timezone = SelectField(
        "Timezone",
        coerce=str,
        validators=[DataRequired()],
        render_kw={"placeholder": " "},
    )
    tax_percentage = FloatField(
        "Tax Percentage", render_kw={"placeholder": "0.00"}, default=0.00
    )

    def __init__(self, **kwargs):
        super(RestaurantForm, self).__init__(**kwargs)
        all_timezones = get_all_timezones()
        all_currencies = list_currencies()
        self.timezone.choices = all_timezones
        self.currency.choices = [(currency, currency) for currency in all_currencies]
        if "obj" in kwargs and kwargs["obj"] is not None:
            self.tax_percentage.data = float(kwargs["obj"].tax_percentage) / 100
