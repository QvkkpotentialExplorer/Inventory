from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, NumberRange,ValidationError
from data.db_session import db_sess
from data.inventory_type import InventoryType


class InventoryRequestForm(FlaskForm):
    def validate_count(form,field):
        if field.data>100:
            raise ValidationError('Количество предметов в одной заявки не может превышать 100 шт')
    inventory_type_id = SelectField('Инвентарь', coerce=int, validators=[DataRequired()])
    count = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Создать заявку')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем список доступного инвентаря
        self.inventory_type_id.choices = [
            (item.id, item.name) for item in db_sess.query(InventoryType).all()
        ]