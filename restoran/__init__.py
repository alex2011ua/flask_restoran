from flask import Flask

from example1.config import Config
from example1.models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from example1.views import *
