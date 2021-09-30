from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Первый аргумент - метка или описание поля
                                                                    # Второй аргумент - validators - привязывает к полю проверку данных
                                                                    # DataRequired()  - валидатор проверяет, что поле не отправлено пустым
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()]) # Валидатор Email() проверяет содержимое поля на
                                                                       # соответсвие структуре адреса электронной почты
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')]) # Валидатор EqualTo() проверяет
                                                                                                         # содержимое поля на соответствие
                                                                                                         # содержимому поля password
    submit = SubmitField('Register')

    # Когда добавляются методы, соответствующие шаблону validate_<имя_поля>, WTForms принимает их как пользовательские валидаторы
    # и вызывает их в дополнение к стандартным валидаторам
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # Ищем пользователя с указанным именем в БД
        if user is not None:                                        # Если в БД есть совпадение, значит зарегистрировать такого пользователя не можем
            raise ValidationError('Please use a different username') # Инструкция raise возбуждает указанное исключение
                                                                     # ValidationError() инициирует ошибку. Сообщение, переданное
                                                                     # в качестве аргумента будет отображаться рядом с полем для просмотра

    def validate_email(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class EditProfileForm(FlaskForm):
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg'])]) # Валидатор FileAllowed() пропускает только
                                                                    # файлы, указанного расширения
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)]) # Валидатор Length() проверяет, чтобы введенный
                                                                              # текст был от 0 до 140 символов
    submit = SubmitField('Submit')

    original_username = StringField()

    def __init__(self, original_username): # Конструктор класса принимает старое имя пользователя в качестве аргумента
        super().__init__() # Функция super() позволяет вызвать одноименный метод из базового класса
                           # Происходит вызов конструктора из базового класса FlaskForm,
                           # после чего выполняется конструктор наследника EditProfileForm

        self.original_username = original_username # Сохраняем старое имя, оно понадобится в validate_username

    def validate_username(self, username): # Валидатор проверяет, чтобы в БД не было записи с таким же именем пользователя
        if username.data != self.original_username:                          # Если, новое имя не совпадает со старым,
            user = User.query.filter_by(username=self.username.data).first() # ищем свопадения нового имени с БД
            if user is not None:                                             # и, если находим,
                raise ValidationError('Please, use a different username')    # то генерируем исключение