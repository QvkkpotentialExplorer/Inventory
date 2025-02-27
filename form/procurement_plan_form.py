from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DecimalField, DateField,SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from data.db_session import db_sess
from data.inventory_type import InventoryType

class ProcurementPlanForm(FlaskForm):
    @staticmethod
    def get_inventory_type():
        return [name[0] for name in db_sess.query(InventoryType.name).all()]

    def validate_count(form,field):
        if field.data>10000:
            raise ValidationError("Количество предметов для закупки не может превышать 10000 шт ")

    inventory_type = SelectField('Тип инвентаря', validators=[DataRequired()], choices=get_inventory_type())
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1,max = 10000)])
    price = DecimalField('Цена за единицу', validators=[DataRequired(), NumberRange(min=1,max =200000)])
    supplier = StringField('Поставщик', validators=[DataRequired()])
    planned_date = DateField('Дата планирования', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Создать план закупок')
