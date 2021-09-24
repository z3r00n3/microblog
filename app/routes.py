from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required # защищаем страницу от просмотра неаутентифицированными пользователями
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beatifull day on Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts) # render_template() - функция рендеринга шаблона,
                                                                               # принимает имя файла шаблона и список аргументов
                                                                               # шаблона (заполнители шаблона)

@app.route('/login', methods=['GET', 'POST']) # methods=['GET', 'POST']) сообщает, что по этому URL принимаются GET и POST запросы,
                                              # по умолчанию, без указания этого параметра используется GET
                                              # POST - обычно используется, когда браузер передает данные формы на сервер
def login():
    if current_user.is_authenticated: # current_user поступает из Flask-Login и используется для получения объекта пользователя
                                      # is_authenticated - свойство пользовательского объекта, унаследованное от класса UserMixin
                                      # из Flask-Login, позволяющее проверить, зарегистрирован ли пользователь
        return redirect(url_for('index')) # redirect() - автоматический переход на другую страницу
                                          # url_for() - генерирует URL-адрес
    form = LoginForm()
    if form.validate_on_submit(): # метод validate_on_submit() выполняет обработку формы: собирает все данные, запускает все валидаторы
        user = User.query.filter_by(username=form.username.data).first() # имя пользователя пришло с формой отправки, поэтому можно
                                                                         # запросить БД, чтобы найти его
                                                                         # filter_by() - возвращает объекты с совпадающими именами
                                                                         # first() - вернет первый объект из очереди или None, если пусто
        if user is None or not user.check_password(form.password.data): # проверяем, существует ли пользователь с указанным именем и
                                                                        # соответствует ли введенный из формы пароль хешу пароля из БД
            flash('Invalid username or password') # выводит сообщение в случае неудачи
            return redirect(url_for('login')) # и перенаправляет на повторный вход
        login_user(user, remember=form.remember_me.data) # в случае удачной проверки регистрируем вход пользователя в систему
                                                         # с помощью login_user() из Flask-Login. После этого для данного
                                                         # пользователя устанавливается переменная current_user из Flask-Login
                                                         # и она будет доступна на любых будущих страницах, которые посетит пользователь
        next_page = request.args.get('next') # request - предоставляет строку запроса
                                             # args - предоставляет эту же строку запроса, но уже в виде словаря
        if not next_page or url_parse(next_page).netloc != '': # url_parse() из Werkzeug анализирует next_page, а затем идет
                                                               # проверка, установлен ли компонент netloc (network location -
                                                               # упрощенно доменное имя). Это позволяет понять, является URL
                                                               # относительныи или абсолютным. Это нужно из соображений безопасности,
                                                               # т.к. злоумышленник может подставить в аргумент next строки запроса
                                                               # URL-адрес злоумышленного сайта
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user() # logout_user() - функция Flask-Login для выхода текущего пользователя из системы
    return redirect(url_for('index'))

@app.route('/user/<name>') # <name> - переменная для формирования динамического пути; передаётся в функцию, как параметр name
def user(name):
    return '<h3>Hello, {}!</h3>'.format(name) # format(name) - метод подставляет в строку значение name вместо {}