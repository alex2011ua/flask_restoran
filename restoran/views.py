from functools import wraps

from flask import abort, flash, session, redirect, request, render_template

from example1 import app, db
from example1.models import User
from example1.forms import LoginForm, RegistrationForm, ChangePasswordForm

# ------------------------------------------------------
# Декораторы авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("login_required")
        if not session.get('user'):
            return redirect('/login')	
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("admin_only")
        if session.get('user')["role"] != "admin":
            abort(403, description="Вам сюда нельзя")
        return f(*args, **kwargs)
    return decorated_function

# ------------------------------------------------------
# Страница админки
@app.route('/')
@login_required 
def home():
    return render_template("page_admin.html")

# ------------------------------------------------------
# Страница аутентификации
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect("/")

    form = LoginForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("page_login.html", form=form)
        
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_valid(form.password.data):
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
            return redirect("/")

        form.username.errors.append("Не верное имя или пароль")

    return render_template("page_login.html", form=form)

# ------------------------------------------------------
# Страница выхода из админки
@app.route('/logout', methods=["POST"])
@login_required 
def logout():
    session.pop("user")
    return redirect("/login")

# ------------------------------------------------------
# Страница добавления пользователя
@app.route("/registration", methods=["GET", "POST"])
@admin_only
@login_required 
def registration():
    form = RegistrationForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("page_registration.html", form=form)

        user = User.query.filter_by(username=form.username.data).first()
        if user:
            form.username.errors.append("Пользователь с таким именем уже существует")
            return render_template("page_registration.html", form=form)

        user = User()
        user.username = form.username.data
        user.password = form.password.data
        user.role = "user"
        db.session.add(user)
        db.session.commit()

        flash(f"Пользователь: {form.username.data} с паролем: {form.password.data} зарегистрирован")
        return redirect("/registration")

    return render_template("page_registration.html", form=form)

# ------------------------------------------------------
# Страница смены пароля
@app.route("/change-password", methods=["GET", "POST"])
@login_required 
def change_password():
    form = ChangePasswordForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # Обновляем пароль у текущего пользователя по его идентификатору
            user = User.query.filter_by(id=session["user"]["id"]).first()
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()

            flash(f"Ваш пароль изменён")
            return redirect("/change-password")

    return render_template("change_password.html", form=form)
