from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
        DataRequired(), 
        Length(min=8, message='Пароль должен содержать не менее 8 символов')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), 
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться') 