from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, FileField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from data.db_session import db_sess
from data.user import User


class InventoryReportForm(FlaskForm):
    @staticmethod
    def get_users():
        print([name[0] for name in db_sess.query(User.username).all()])
        return list([user.username for user in db_sess.query(User).all()])

    def validate_description(form, field):
        if len(field.data) >350:
            raise ValidationError("Текст отчета не может превышать 350 символов")

    inventory_id = IntegerField('ID Инвентаря', validators=[DataRequired()])
    condition_before = SelectField(
        'Состояние до использования',
        choices=[('new', 'Новое'), ('used', 'Использованное'), ('broken', 'Сломанное')],
        validators=[DataRequired()]
    )
    condition_after = SelectField(
        'Состояние после использования',
        choices=[('new', 'Новое'), ('used', 'Использованное'), ('broken', 'Сломанное')],
        validators=[DataRequired()]
    )
    description = StringField(validators=[DataRequired(), validate_description])
    photo = FileField('Фото', validators=[DataRequired()])
    user = SelectField(choices = get_users() )
    submit = SubmitField('Добавить отчёт')

