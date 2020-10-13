from flask import Flask

from flask_migrate import Migrate

from restoran.config import Config
from restoran.models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from restoran.views import *
