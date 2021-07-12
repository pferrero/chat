import functools
from chatapp import db, socketio
from chatapp.models import User, Message, Open_chat
from flask_login import current_user
from flask_socketio import emit, rooms, join_room, disconnect


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on("connect")
@authenticated_only
def connect_user():
    print("New connection: " + current_user.username)


@socketio.on("disconnect")
def disconnect_user():
    print("Client disconnected: " + current_user.username)


@socketio.event
@authenticated_only
def send_msg(message):
    print("Event: send_msg. User: ", current_user)
    print("Data received: ", message["data"])
    user = User.query.filter_by(username=message["username"]).first()
    msg = message["data"]
    # Check if there is an open chat with that user already
    open_chat = Open_chat.query.filter(
        db.or_(
            db.and_(Open_chat.user1 == current_user, Open_chat.user2 == user),
            db.and_(Open_chat.user1 == user,
                    Open_chat.user2 == current_user))).first()
    if open_chat is None:
        # Save de open chat
        open_chat = Open_chat(user1=current_user, user2=user)
        db.session.add(open_chat)
        # db.session.commit()
    # Save the message
    new_msg = Message(from_user=current_user, to_user=user, body=msg)
    db.session.add(new_msg)
    db.session.commit()
    # Check if the user is in the room
    room_name = "-".join((open_chat.user1.username, open_chat.user2.username))
    if room_name not in rooms():
        join_room(room_name)
    # Emit the new message to the room
    emit("new_msg", {
        "name": new_msg.from_user.username,
        "body": new_msg.body,
        "time": new_msg.timestamp.isoformat()
    },
         to=room_name)
