from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class AddInventoryReplacementForm(FlaskForm):
    def validate_description(form,field):
        if len(field.data)>300:
            raise ValidationError("Текст заявки не должен превышать 300 символов")
    inventory_id = IntegerField()
    reason_description = StringField(validators=[DataRequired()])
    submit = SubmitField('Отправить заявку на замену')