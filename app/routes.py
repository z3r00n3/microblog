from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from datetime import datetime

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
                                      # из Flask-Login, позволяющее проверить, аутентифицирован ли пользователь
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

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data) # создаем объект пользователя с данными из формы
        user.set_password(form.password.data)
        # все изменения в БД происходят в контексте сеанса, к которому можно получить доступ с помощью db.session
        # сеансы гарантируют, что БД никогда не останется в несогласованном состоянии
        # эти изменения накапливаются с помощью db.session.add(), а фактически записываются при вызове db.session.commit(),
        # т.е. можно накапливать изменения, а потом их все атомарно разом записать
        # откатить изменения можно с помощью db.session.rollback()
        db.session.add(user) # добавляем нового пользователя в объект БД
        db.session.commit() # записываем изменения в БД
        flash('Congratulations, you are now registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)

@app.route('/logout')
def logout():
    logout_user() # logout_user() - функция Flask-Login для выхода текущего пользователя из системы
    return redirect(url_for('index'))

@app.route('/user/<username>') # <username> - динамический компонент URL-адреса; передаётся в функцию, как параметр username
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404() # first_or_404() работает также как first(), когда есть результат,
                                                                  # но в случае его отсутствия будет вызвано исключение, и клиенту
                                                                  # вернется ошибка 404
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit(): # validate_on_submit() вернет True, если были пройдены все проверки полей и отправляется запрос POST
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
#        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.before_request # Декоратор регистрирует функцию, которая должна быть выполнена всякий раз, как пользователь отправляет
                    # запрос на сервер, то есть до того, как будет вызвана какая-либо функция представления
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
























