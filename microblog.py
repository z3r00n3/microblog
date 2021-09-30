from app import app, db
from app.models import User, Post
import os

# Декоратор @app.shell_context_processor регистрирует функцию контекста оболочки
# Команда flask shell будет ее вызывать и регистрировать элементы, возвращаемые ею в сеансе оболочки
# Сама функция создает контекст оболочки, который добавляет экземпляр и модели БД в сеанс оболочки,
# что позволяет не заниматься их импортом вручную
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    # host='0.0.0.0' - даёт публичный доступ к серверу
    # debug=True - включить режим отладки, что позволяет обновлять страницы по мере обновления кода