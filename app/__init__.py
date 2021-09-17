# В Python, подкаталог, содержащий файл __init__.py, считается пакетом и может быть импортирован

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config) # приложение читает и применяет конфигурацию
db = SQLAlchemy(app) # объект Базы Данных
migrate = Migrate(app, db) # объект механизма миграции

from app import routes, models