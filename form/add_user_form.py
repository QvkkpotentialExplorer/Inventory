from flask_wtf import FlaskForm
from wtforms import  IntegerField, SubmitField, StringField,SelectField,EmailField
from wtforms.validators import DataRequired

from data.db_session import db_sess
from data.inventory_type import InventoryType

class AddUserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])
    role = SelectField(choices=('user','admin'))
    fullname = StringField(validators=[DataRequired()])

    submit = SubmitField('Создать')