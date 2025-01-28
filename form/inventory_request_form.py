from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, NumberRange
from data.db_session import db_sess
from data.inventory import Inventory

class InventoryRequestForm(FlaskForm):
    inventory_id = SelectField('Инвентарь', coerce=int, validators=[DataRequired()])
    count = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Создать заявку')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем список доступного инвентаря
        self.inventory_id.choices = [
            (item.id, item.name) for item in db_sess.query(Inventory).all()
        ]