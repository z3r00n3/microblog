from app import db, login, avatars_url
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

class User(UserMixin, db.Model): # Класс User наследует от db.Model, базового класса для всех моделей из Flask-SQLAlchemy
                                 # Класс User наследует от класса UserMixin из Flask-Login, который включает в себя все необходимые общие реализации,
                                 # а именно четыре обязательных элемента: свойства is_authenticated, is_active, is_anonymous и метод get_id()
    id = db.Column(db.Integer, primary_key=True) # primary_key - первичный ключ
    username = db.Column(db.String(64), index=True, unique=True) # поле должно и индексироваться и быть уникальным
    email = db.Column(db.String(120), index=True, unique=True)   # поле должно и индексироваться и быть уникальным
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # Это не фактическое поле БД, а высокоуровневое представление о
                                                                      # взаимотношениях между user и post. Связь "один ко многим", т.е.
                                                                      # один user - много post
                                                                      # db.relationship определяется на стороне "один", а первый аргумент
                                                                      # указывает класс, который представляет сторону "много"
                                                                      # backref - определяет имя поля (виртуального), которое будет добавлено
                                                                      # к объектам класса "много", который указывает на объект "один"
                                                                      # lazy    - определяет, как будет выполняться запрос БД для связи
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # __repr__() сообщает Python, как надо печатать объекты данного класса, полезно при отладке
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self):
        if os.path.exists(os.path.abspath(os.path.dirname(__file__) + '{}{}.jpg'.format(avatars_url, self.id))):
            return '{}{}.jpg'.format(avatars_url, self.id)
        else:
            return '{}default_avatar.jpg'.format(avatars_url)

@login.user_loader # Декоратор @login.user_loader регистрирует пользовательский загрузчик во Flask-Login,
                   # с помощью этой функции в current_user оказывается текущий пользователь
def load_user(id):
    return User.query.get(int(id)) # id, который передается из Flask-Login является строкой, поэтому преобразование в int

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # Проиндексировано, чтобы можно было получать сообщения
                                                                            # в хронологическом порядке. Аргументу по умолчанию (default)
                                                                            # передана функция datetime.utcnow и SQLAlchemy установит для
                                                                            # поля значение вызова этой функции. После utcnow не стоит
                                                                            # оператор вызова функции (), и поэтому полю присваивается не
                                                                            # результат вызова функции, а сама функция
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # поле user_id называется внешним ключом и служит для связи данного
                                                              # поля с полем id из таблицы user (написание именно в нижнем регистре)

    def __repr__(self):
        return '<Post {}>'.format(self.body)