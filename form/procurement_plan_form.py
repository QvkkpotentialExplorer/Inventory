from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DecimalField, DateField,SelectField
from wtforms.validators import DataRequired, NumberRange
from data.db_session import db_sess
from data.inventory_type import InventoryType

class ProcurementPlanForm(FlaskForm):
    @staticmethod
    def get_inventory_type():
        return [name[0] for name in db_sess.query(InventoryType.name).all()]
    inventory_type = SelectField('Тип инвентаря', validators=[DataRequired()], choices=get_inventory_type())
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    price = DecimalField('Цена за единицу', validators=[DataRequired(), NumberRange(min=0)])
    supplier = StringField('Поставщик', validators=[DataRequired()])
    planned_date = DateField('Дата планирования', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Создать план закупок')
