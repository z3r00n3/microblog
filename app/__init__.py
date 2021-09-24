# В Python, подкаталог, содержащий файл __init__.py, считается пакетом и может быть импортирован

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config) # приложение читает и применяет конфигурацию
db = SQLAlchemy(app) # объект Базы Данных
migrate = Migrate(app, db) # объект механизма миграции
login = LoginManager(app)
login.login_view = 'login' # Flask-Login предоставляет функцию, которая заставляет пользователей регистрироваться,
                           # прежде, чем они смогут просматривать определенные страницы. Защитить эти страницы от
                           # просмотра можно с помощью декоратора @login_required перед функцией просмотра
                           # login_view нужно присвоить имя функции для входа в систему, именно на нее будет
                           # происходить перенаправление при попытке просмотра защищенной страницы. При перенаправлении
                           # будет добавлен аргумент строки запроса next, в котором будет содержаться URL-адрес страницы,
                           # которую пользователь хотел просмотреть. После успешного входа он будет на нее перенаправлен
                           # Обработку этого аргумента см. в routes.py в функции login()

from app import routes, models