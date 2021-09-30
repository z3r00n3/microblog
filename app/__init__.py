# В Python, подкаталог, содержащий файл __init__.py, считается пакетом и может быть импортирован

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler, SMTPHandler
import logging
import os

app = Flask(__name__)
app.config.from_object(Config) # Приложение читает и применяет конфигурацию
db = SQLAlchemy(app) # Объект Базы Данных
migrate = Migrate(app, db) # Объект механизма миграции
login = LoginManager(app)
login.login_view = 'login' # Flask-Login предоставляет функцию, которая заставляет пользователей регистрироваться,
                           # прежде, чем они смогут просматривать определенные страницы. Защитить эти страницы от
                           # просмотра можно с помощью декоратора @login_required перед функцией просмотра.
                           # login_view нужно присвоить имя функции для входа в систему, именно на нее будет
                           # происходить перенаправление при попытке просмотра защищенной страницы. При перенаправлении
                           # будет добавлен аргумент строки запроса next, в котором будет содержаться URL-адрес страницы,
                           # которую пользователь хотел просмотреть. После успешного входа он будет на нее перенаправлен
                           # Обработку этого аргумента см. в routes.py в функции login()
avatars_url = '/static/images/avatars/'

if not app.debug: # Только только при выключенном режиме отладки
    # Отправка email с сообщением об ошибке и логами
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = SMTPHandler( # Создание экземпляра SMTPHandler
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.ERROR) # Отправка сообщений только об ошибках и выше по уровню
        app.logger.addHandler(mail_handler) # Прикрепляем mail_handler к логгеру из Flask

    # Запись логов в журнал
    logs_url = os.path.abspath(os.path.dirname(__file__) + '/logs')
    if not os.path.exists(logs_url):        # Если папки для логов не существует
        os.mkdir(os.path.abspath(logs_url)) # Создаем ее
    file_handler = RotatingFileHandler( # RotatingFileHandler удобен тем, что он переписывает журналы, гарантируя,
                                        # что файлы журнала не будут слишком большими, если приложение работает в
                                        # течение длительного времени
        logs_url + '/microblog.log', maxBytes=10240, backupCount=10) # maxBytes - максимальный объем журнала
                                                                     # backupCount -максимальное количество журналов

    file_handler.setFormatter(logging.Formatter( # Настройка формата сообщений журнала
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO) # Устанавливаем уровень ведения журнала
                                        # DEBUG    - сообщения всех уровней
                                        # INFO     - сообщения всех уровней, кроме отладочных
                                        # WARNING  - только пердупреждения, ошибки и критические ошибки
                                        # ERROR    - только пердупреждения и критические ошибки
                                        # CRITICAL - только критические ошибки
    app.logger.addHandler(file_handler) # Прикрепляем file_handler к логгеру из Flask

    app.logger.setLevel(logging.INFO) # Отправка только информационных сообщений и выше по уровню
    app.logger.info('MultiBlog Run') # Записываем в журнал момент запуска приложения

from app import routes, models, errors




















