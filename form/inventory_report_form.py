from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class InventoryReportForm(FlaskForm):
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
    photo = FileField('Фото', validators=[DataRequired()])
    submit = SubmitField('Добавить отчёт')
