from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError


class RedactInventoryTypeForm(FlaskForm):
    def validate_max_length_description(form, field):
        if len(field.data) > 200:
            raise ValidationError("Описание типа инвентаря не должно превышать 200 символов")

    def validate_max_length_name(form, field):
        if len(field.data) > 35:
            raise ValidationError("Количество символов в имени не должно быть больше 35")
    name = StringField('Название',validators=[validate_max_length_name])
    description = StringField('Описание',validators=[validate_max_length_description])
    submit = SubmitField('Изменить')
