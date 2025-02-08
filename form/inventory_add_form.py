from flask_wtf import FlaskForm
from wtforms import  IntegerField, SubmitField, StringField,SelectField
from wtforms.validators import DataRequired, ValidationError

from data.db_session import db_sess
from data.inventory_type import InventoryType


class AddInventoryTypeForm(FlaskForm):
    def validate_name(form,field):
        if len(field.data) > 35:
            raise ValidationError("Количество символов в имени не должно быть больше 35")
    def validate_description(form,field):
        if len(field.data) > 200:
            raise ValidationError("Описание типа инвентаря не должно превышать 200 символов")
    name = StringField('Название',validators=[DataRequired(),validate_name])
    description = StringField('Описание',validators=[DataRequired()])
    submit = SubmitField('Создать')

class AddInventoryForm(FlaskForm):
    @staticmethod
    def get_inventory_type():
        print([name[0] for name in db_sess.query(InventoryType.name).all()])
        return [name[0] for name in db_sess.query(InventoryType.name).all()]
    def validate_count(form, field):
        if field.data > 100:
            raise ValidationError("Количество инвентарей в заявке не может быть больше 100.")

    print(db_sess.query(InventoryType.name).all())
    inventory_type = SelectField('Тип инвентаря', validators=[DataRequired()],choices= get_inventory_type())
    count = IntegerField('Количество', validators=[DataRequired(), validate_count])
    submit = SubmitField('Создать')

class InventoryTypeRedactForm(FlaskForm):
    def validate_max_length_description(form,field):
        if len(field.data) >200:
            raise ValidationError("Описание типа инвентаря не должно превышать 200 символов")

    def validate_max_length_name(form, field):
        if len(field.data) > 35:
            raise ValidationError("Количество символов в имени не должно быть больше 35")
    name = StringField(validators=[validate_max_length_name])
    description = StringField(validators=[DataRequired(),validate_max_length_description])
    submit = SubmitField('Изменить')