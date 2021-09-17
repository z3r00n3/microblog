from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'z3r0n3'}
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
    # render_template() - функция рендеринга шаблона, принимает имя файла шаблона и список аргументов шаблона (заполнители шаблона)
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST']) # methods=['GET', 'POST']) сообщает, что по этому URL принимаются GET и POST запросы,
                                              # по умолчанию, без указания этого параметра используется GET
                                              # POST - обычно используется, когда браузер передает данные формы на сервер
def login():
    form = LoginForm()
    if form.validate_on_submit(): # метод validate_on_submit() выполняет обработку формы: собирает все данные, запускает все валидаторы
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data)) # выводит сообщение
        return redirect(url_for('index')) # redirect() - автоматический переход на другую страницу
                                          # url_for() - генерирует URL-адрес
    return render_template('login.html', title='Sign In', form=form)


@app.route('/user/<name>') # <name> - переменная для формирования динамического пути; передаётся в функцию, как параметр name
def user(name):
    return '<h3>Hello, {}!</h3>'.format(name) # format(name) - метод подставляет в строку значение name вместо {}