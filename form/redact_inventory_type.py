from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class RedactInventoryTypeForm(FlaskForm):
    name = StringField('Название')
    description = StringField('Описание')
    submit = SubmitField('Изменить')
