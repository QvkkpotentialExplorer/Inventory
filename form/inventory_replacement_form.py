from flask_wtf import FlaskForm
from wtforms import StringField,HiddenField
from wtforms.validators import DataRequired


class AddInventoryReplacementForm(FlaskForm):
    inventory_id = HiddenField()
    reason_description = StringField(validators=[DataRequired()])