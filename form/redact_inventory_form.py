from flask_wtf import FlaskForm
from wtforms import  IntegerField, SubmitField, StringField,SelectField
from wtforms.validators import DataRequired

from data.db_session import db_sess
from data.inventory_type import InventoryType

class RedactInventoryForm(FlaskForm):
    @staticmethod
    def get_inventory_type():
        return [name[0] for name in db_sess.query(InventoryType.name).all()]
    print(db_sess.query(InventoryType.name).all())
    inventory_type = SelectField('Тип инвентаря', validators=[DataRequired()],choices= get_inventory_type())
    count = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Изменить')

