import hashlib
import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from data.db_session import create_session
from data.models import User, Work
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.add_work_form import AddWorkForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# Функция для хеширования паролей
def hash_password(password):
    salt = os.urandom(16)  # Генерация случайной соли
    password_salt = password.encode('utf-8') + salt
    password_hash = hashlib.sha256(password_salt).hexdigest()  # Хеширование пароля с солью
    return password_hash, salt

# Функция для проверки пароля
def check_password(stored_hash, stored_salt, password):
    password_salt = password.encode('utf-8') + stored_salt
    password_hash = hashlib.sha256(password_salt).hexdigest()
    return password_hash == stored_hash  # Сравнение хеша пароля с сохранённым хешем

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password(user.password, user.salt, form.password.data):  # Проверка пароля
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', form=form, message="Неправильный логин или пароль")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash, salt = hash_password(form.password.data)  # Хешируем пароль
        user = User(email=form.email.data, password=password_hash, salt=salt, name=form.name.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_work', methods=['GET', 'POST'])
@login_required
def add_work():
    form = AddWorkForm()
    if form.validate_on_submit():
        new_work = Work(
            job_title=form.job_title.data,
            team_leader_id=form.team_leader_id.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_job_finished=form.is_job_finished.data
        )
        db.session.add(new_work)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_work.html', form=form)

@app.route('/')
def index():
    works = Work.query.all()
    return render_template('index.html', works=works)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
