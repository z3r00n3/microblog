from datetime import datetime
from app import db

# Класс User наследует от db.Model, базового класса для всех моделей из Flask-SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary_key - первичный ключ
    username = db.Column(db.String(64), index=True, unique=True) # поле должно и индексироваться и быть уникальным
    email = db.Column(db.String(120), index=True, unique=True) # поле должно и индексироваться и быть уникальным
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # это не фактическое поле БД, а высокоуровневое представление о
                                                                      # взаимотношениях между user и post. Связь "один ко многим", т.е.
                                                                      # один user - много post
                                                                      # db.relationship определяется на стороне "один", а первый аргумент
                                                                      # указывает класс, который представляет сторону "много"
                                                                      # backref - определяет имя поля, которое будет добавлено к объектам
                                                                      # класса "много", который указывает на объект "один"
                                                                      # lazy - определяет, как будет выполняться запрос БД для связи

    # __repr__() сообщает Python, как надо печатать объекты данного класса, полезно при отладке
    def __repr__(self):
        return '<User {}>'.format(self.username)

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