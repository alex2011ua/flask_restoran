from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    orders = db.relationship("Order")
    orders_id = db.Column(db.Integer, db.ForeignKey("orders.id"))


    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.DECIMAL(20, 2), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    picture = db.Column(db.String(128), nullable=False)
    category = db.relationship("Category")
    category_id = db.Column(db.Integer, db.ForeignKey("meals.id"))


class Category(db.Model):
    __tablename__ = 'categorys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable = False, unique = True)
    meals = db.relationship("Meal")

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    summ = db.Column(db.DECIMAL(20, 2), nullable = False)
    status = db.Column(db.String(128))
    email = db.Column(db.String(32))
    tel = db.Column(db.Integer())
    addres = db.Column(db.String(128))
    meails_list = db.Column(db.String(128))
    
