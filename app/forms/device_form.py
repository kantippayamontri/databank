from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class DeviceForm(FlaskForm):
    device_name = StringField(
        "Choose your device name: ",
        validators=[DataRequired(), Length(1, 40)],
    )
    submit = SubmitField("Submit")
