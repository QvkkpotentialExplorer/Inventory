from flask_wtf import FlaskForm
from wtforms import  IntegerField, SubmitField, StringField,SelectField
from wtforms.validators import DataRequired, ValidationError

from data.db_session import db_sess
from data.inventory_type import InventoryType


class AddInventoryTypeForm(FlaskForm):
    name = StringField('Название',validators=[DataRequired()])
    description = StringField('Описание',validators=[DataRequired()])
    submit = SubmitField('Создать')

class AddInventoryForm(FlaskForm):
    @staticmethod
    def get_inventory_type():
        print([name[0] for name in db_sess.query(InventoryType.name).all()])
        return [name[0] for name in db_sess.query(InventoryType.name).all()]
    def validate_count(form, field):
        if field.data > 100:
            raise ValidationError("Количество не может быть больше 100.")

    print(db_sess.query(InventoryType.name).all())
    inventory_type = SelectField('Тип инвентаря', validators=[DataRequired()],choices= get_inventory_type())
    count = IntegerField('Количество', validators=[DataRequired(), validate_count])
    submit = SubmitField('Создать')

