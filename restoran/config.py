import os
from os import environ


username = environ.get('usr')
password = environ.get('pass')
servername = environ.get('host')
db_name = environ.get('db_name')


class Config:

    SECRET_KEY = environ.get('secret_key')
    SQLALCHEMY_DATABASE_URI = f'mysql://{username}:{password}@{servername}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
