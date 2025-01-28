
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from data.user import User
from data.db_session import db_sess


def validate_login(form, data):
    val_log = db_sess.query(User).filter(User.username == data.data).first()
    if val_log:
        raise ValidationError('Этот логин уже занят , придумайте другой')



class RegisterForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), validate_login])
    fullname = StringField('Полное имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('confirm', message='Пароли не совпадают')])
    confirm = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')
