from chatapp import app, db
from chatapp.models import User, Message, Open_chat


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Message": Message,
        "Open_chat": Open_chat
    }
