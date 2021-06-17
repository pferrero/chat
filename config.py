import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or \
        b'8B\x89f\xf0\x89\xa0\xfb\xdb+\xacDma\xb9?'

    PERMANENT_SESSION_LIFETIME = os.environ.get("PERMANENT_SESSION_LIFETIME") or \
        timedelta(minutes=30)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "chat.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False