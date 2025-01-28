from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired, NumberRange
from data.db_session import db_sess
from data.inventory_type import InventoryType

class ProcurementPlanForm(FlaskForm):
    inventory_type = StringField('Тип инвентаря', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    price = DecimalField('Цена за единицу', validators=[DataRequired(), NumberRange(min=0)])
    supplier = StringField('Поставщик', validators=[DataRequired()])
    planned_date = DateField('Дата планирования', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Создать план закупок')
