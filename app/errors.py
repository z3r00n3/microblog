from flask import render_template
from app import app, db

@app.errorhandler(404) # Декоратор объявляет пользовательский обработчик ошибок
def not_found_error(error):
    return render_template('404.html'), 404 # Второй параметр - это код HTTP
                                            # Если ничего не указано, то по умолчанию возвращается
                                            # 200 - код состояния для удачного завершения

# Почему-то вызывается обработчик по-умолчанию, хотя перепробовал все способы из документации,
# в том числе и через exception
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500