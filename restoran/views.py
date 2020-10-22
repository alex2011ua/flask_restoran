from functools import wraps
from datetime import datetime
import add_base
from flask import abort, flash, session, redirect, request, render_template, url_for

from restoran import app, db
from restoran.models import User, Category, Meal, Order
from restoran.forms import LoginForm, RegistrationForm, ChangePasswordForm, OrderForm

from flask_admin.contrib.sqla import ModelView

# ------------------------------------------------------
# Декораторы авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("login_required")
        if not session.get('user'):
            return redirect(url_for('login'))
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


@app.route('/account')
@login_required
def account():
    return render_template("account.html")



# ------------------------------------------------------
#clear_cart
@app.route('/cls/')
def clear_cart():
    if session["cart"]:
        del session["cart"]
    if session["count"]:
        del session["count"]
    if session['summ']:
        del session['summ']
    return redirect(url_for('home'))

# Страница админки
@app.route('/')
#@login_required
def home():
    cat = Category.query.all()
    #add_base.add()
    return render_template("main.html",
                           cats = cat,
                           )

#Добавление в карзину
@login_required
@app.route('/addtocart/<id>/')
def addtocart(id):
    meal = Meal.query.get(int(id))
    if session.get("cart"):
        session["cart"].append(id)
        session["count"] += 1
        session['summ'] += float(meal.price)
    else:
        session["cart"] = [id]
        session["count"] = 1
        session['summ'] = float(meal.price)
    flash('Блюдо добавлено!')
    return redirect(url_for('home'))

#Удаление из карзину
@login_required
@app.route('/delfromcart/<id>/')
def delfromcart(id):
    cards = session.get("cart")
    meal = Meal.query.get(int(id))
    cards.remove(id)
    session['cart'] = cards
    session["count"] -= 1
    session['summ'] -= float(meal.price)
    flash('Блюдо удалено из корзины')
    return redirect(url_for('cart'))

#подсчет суммы покупки, список товаров и названий
def count_summ_title_meals():
    list_meals = session.get("cart")
    meals = []
    meals_title = []
    summ_cart = 0
    for item in list_meals:
        meals.append(Meal.query.get(int(item)))
    for meal in meals:
        summ_cart += meal.price
        meals_title.append(meal.title)
    return summ_cart, meals_title, meals

@login_required
@app.route('/cart/', methods=["GET", "POST"])
def cart():
    if session.get("cart"):
        form = OrderForm()
        summ_cart, meals_title, meals = count_summ_title_meals()

        if request.method == "POST":
            if not form.validate_on_submit():
                return render_template("cart.html", form=form, meals = meals, summ_cart = summ_cart)
            user = User.query.filter_by(mail=session.get('user')['mail']).first()
            order = Order()
            order.date = datetime.now()
            order.summ = summ_cart
            order.status = 'new'
            order.email = session.get("user")['mail']
            order.tel = form.tel.data
            order.addres = form.address.data
            order.meails_list = ','.join(meals_title)
            db.session.add(order)
            db.session.commit()
            user.orders_id = order.id
            db.session.commit()
            session["user"]['orders'] = order.id
            flash("Заказ отправлен!")
            return redirect(url_for('clear_cart'))
        return render_template("cart.html", form=form, meals = meals, summ_cart = summ_cart)


    else:
        meals = None
        summ_cart = None
        return render_template("cart.html", meals=meals, summ_cart=summ_cart)


# ------------------------------------------------------
# Страница аутентификации
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for('home'))

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
                'orders': user.orders_id
            }
            return redirect(url_for('home'))

        form.mail.errors.append("Не верное имя или пароль")

    return render_template("login.html", form=form)

# ------------------------------------------------------
# Страница выхода из админки
@app.route('/logout')
@login_required 
def logout():
    session.pop("user")
    return redirect(url_for('home'))


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
        return redirect(url_for('home'))

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
            return redirect(url_for('home'))

    return render_template("change_password.html", form=form)




class MyUserView(ModelView):
    def is_accessible(self):
        if not session.get('user'):
            return None
        if session.get('user')["role"] != "admin":
            return None
        return True


    # прочие свойства