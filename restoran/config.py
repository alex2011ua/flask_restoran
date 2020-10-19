import os

current_path = os.path.dirname(os.path.realpath(__file__))
db_path = "sqlite:///" + current_path + "\\test1.db"

class Config:

    SECRET_KEY= "secret_key"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False