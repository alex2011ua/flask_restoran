from functools import wraps

from flask import abort, flash, session, redirect, request, render_template

from restoran import app, db
from restoran.models import User, Category
from restoran.forms import LoginForm, RegistrationForm, ChangePasswordForm

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
#@login_required
def home():
    cat = Category.query.all()
    return render_template("main.html", cats = cat)

#Добавление в карзину
@login_required
@app.route('/addtocart/<id>/')
def addtocart(id):
    session["cart"] = id
    return redirect("/cart")


@login_required
@app.route('/cart/')
def cart():

    return render_template("cart.html")


# ------------------------------------------------------
# Страница аутентификации
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect("/")

    form = LoginForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("login.html", form=form)
        
        user = User.query.filter_by(mail=form.mail.data).first()
        if user and user.password_valid(form.password.data):
            session["user"] = {
                "id": user.id,
                "mail": user.mail,
                "role": user.role,
            }
            return redirect("/")

        form.username.errors.append("Не верное имя или пароль")

    return render_template("login.html", form=form)

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
#@admin_only
#@login_required
def registration():
    form = RegistrationForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("register.html", form=form)

        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            form.mail.errors.append("Пользователь с таким именем уже существует")
            return render_template("register.html", form=form)

        user = User()
        user.mail = form.mail.data
        user.password = form.password.data
        user.role = "user"
        db.session.add(user)
        db.session.commit()

        flash(f"Пользователь: {form.mail.data} с паролем: {form.password.data} зарегистрирован")
        return redirect("/login")

    return render_template("register.html", form=form)

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
