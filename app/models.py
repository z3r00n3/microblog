from app import db

# Класс User наследует от db.Model, базового класса для всех моделей из Flask-SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary_key - первичный ключ
    username = db.Column(db.String(64), index=True, unique=True) # поле должно и индексироваться и быть уникальным
    email = db.Column(db.String(120), index=True, unique=True) # поле должно и индексироваться и быть уникальным
    password_hash = db.Column(db.String(128))

    # __repr__() сообщает Python, как надо печатать объекты данного класса, полезно при отладке
    def __repr__(self):
        return '<User {}>'.format(self.username)