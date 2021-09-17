from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # первый аргумент - метка или описание поля
    # второй аргумент - validators - привязывает к полю проверку данных
    # DataRequired() - валидатор проверяет, что поле не отправлено пустым
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')