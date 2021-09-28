import os
basedir = os.path.abspath(os.path.dirname(__file__)) # генерация абсолютного пути до основного каталога приложения

# Параметры конфигурации приложения определяются как переменные класса внутри класса Config
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ztdbdtz' # ищет значение переменной среды, если не находит,
                                                           # то использует значение жёстко закодированной строки
                                                           # Flask и некоторые его расширения используют значение
                                                           # секретного ключа для генерации подписей или токенов
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # местоположение БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False # отключает сигнализацию приложению при каждом изменении БД