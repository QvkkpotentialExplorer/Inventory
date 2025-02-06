from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddInventoryReplacementForm(FlaskForm):

    inventory_id = IntegerField()
    reason_description = StringField(validators=[DataRequired()])
    submit = SubmitField('Отправить заявку на замену')