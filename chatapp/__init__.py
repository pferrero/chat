from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'8B\x89f\xf0\x89\xa0\xfb\xdb+\xacDma\xb9?'
app.permanent_session_lifetime = timedelta(days=1)

from chatapp import routes, database