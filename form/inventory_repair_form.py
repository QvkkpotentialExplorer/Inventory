from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class InventoryRepairForm(FlaskForm):
    description = TextAreaField('Описание проблемы', validators=[DataRequired()])
    submit = SubmitField('Отправить заявку на ремонт')
