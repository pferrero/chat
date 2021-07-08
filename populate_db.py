# This script is used to initialize de database
# with some example data.
from chatapp import db
from chatapp.routes import User, Open_chat, Message

# Add users
u1 = User(username="user1", about_me="I love programming.")
u2 = User(username="user2", about_me="Linux enthusiast")
u3 = User(username="user3")

u1.set_password("123456")
u2.set_password("123456")
u3.set_password("123456")

# Open chats between registered users.
oc1 = Open_chat(user1=u1, user2=u2)
oc2 = Open_chat(user1=u1, user2=u3)

# Messages betweem registered users with open chats.
m1 = Message(from_user=u1, to_user=u2, body="Hi!")
m2 = Message(from_user=u2, to_user=u1, body="Hi!, How are you?")
m3 = Message(from_user=u1, to_user=u3, body="Hello!")

# Add changes to the session
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(oc1)
db.session.add(oc2)
db.session.add(m1)
db.session.add(m2)
db.session.add(m3)

# commit the changes to the database
db.session.commit()
