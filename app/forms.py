from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # первый аргумент - метка или описание поля
    # второй аргумент - validators - привязывает к полю проверку данных
    # DataRequired() - валидатор проверяет, что поле не отправлено пустым
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()]) # валидатор Email() проверяет содержимое поля на
                                                                       # соответсвие структуре адреса электронной почты
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')]) # валидатор EqualTo() проверяет
                                                                                                         # содержимое поля на соответствие
                                                                                                         # содержимому поля password
    submit = SubmitField('Register')

    # когда добавляются методы, соответствующие шаблону validate_<имя_поля>, WTForms принимает их как пользовательские валидаторы
    # и вызывает их в дополнение к стандартным валидаторам
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # ищем пользователя с указанным именем в БД
        if user is not None: # Если в БД есть совпадение, значит зарегистрировать такого пользователя не можем
            raise ValidationError('Please use a different username') # инструкция raise возбуждает указанное исключение
                                                                     # ValidationError() инициирует ошибку. Сообщение, переданное
                                                                     # в качестве аргумента будет отображаться рядом с полем для просмотра

    def validate_email(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)]) # валидатор Length() проверяет, чтобы введенный
                                                                              # текст был от 0 до 140 символов
    submit = SubmitField('Submit')