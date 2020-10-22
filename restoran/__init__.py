from flask import Flask

from flask_migrate import Migrate

from restoran.config import Config
from restoran.models import db

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)



from restoran.views import *

admin = Admin(app)



admin.add_view(MyUserView(User, db.session))
admin.add_view(MyUserView(Meal, db.session))
admin.add_view(MyUserView(Category, db.session))
admin.add_view(MyUserView(Order, db.session))