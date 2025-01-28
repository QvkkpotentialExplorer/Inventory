from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from data.db_session import create_engine_and_session
from data.user import User
from data.db_session import db_sess

def validate_password(form, data):
    val = db_sess.query(User).filter(User.username == form.username.data).first()
    if not val :
        raise ValidationError('Пользователя с таким ником нет')
    elif not val.check_password(form.password.data):
        raise ValidationError('Неверный пароль')


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired(), validate_password])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')