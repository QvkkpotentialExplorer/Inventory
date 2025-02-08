from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class InventoryRepairForm(FlaskForm):
    def validate_description(form,field):
        if len(field.data)>300:
            raise ValidationError("Описание поломки не должно превышать 300 символов")
    description = TextAreaField('Описание проблемы', validators=[DataRequired(),validate_description])
    submit = SubmitField('Отправить заявку на ремонт')
