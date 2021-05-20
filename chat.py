from datetime import timedelta
from flask import Flask, request, url_for, render_template, redirect, abort, session, flash, jsonify
import database

USERNAME_KEY = "logged_user"
CHATWITH_KEY = ""

app = Flask(__name__)
app.secret_key = b'8B\x89f\xf0\x89\xa0\xfb\xdb+\xacDma\xb9?'
app.permanent_session_lifetime = timedelta(days=1)

@app.route('/')
def index():
    """
    Displays index page.
    If the user has an active session it redirects the request to home.
    """
    if USERNAME_KEY not in session:
        return render_template('index.html.jinja',
                                signup_link=url_for("signup"),
                                login_link=url_for("login"))
    else:
        return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Displays login page if it's a GET request.
    Tries to log user in if it's a POST request.
    """
    if request.method == "GET":
        return render_template("login.html.jinja",
                                process_login=url_for("login"))
    elif request.method == "POST":
        return login_user(request.form.get("txtUser", default=None),
                          request.form.get("txtPass", default=None))
        
def login_user(username, password):
    """
    Tries to log user in.
    """
    if username == None or password == None:
        abort(400)
    else:
        login = database.check_login(username, password)
        if login:
            session[USERNAME_KEY] = username
            session.permanent = True
            flash(f"Successufully logged in as {username}")
            return redirect(url_for("home"))
        else:
            flash(f"Invalid user or password")
            return redirect(url_for("login"))

@app.route("/logout")
def logout():
    """
    Terminates the user session and redirects to index.
    """
    session.pop(USERNAME_KEY)
    session.pop(CHATWITH_KEY)
    flash("You were successfully logged out.")
    return redirect(url_for("index"))

@app.route("/singup", methods=["GET", "POST"])
def signup():
    """
    Displays signup page if it's a GET request.
    Tries to sign the user up if it's a POST request.
    """
    if request.method == "GET":
        return render_template("singup.html.jinja",
                                signup_link=url_for("signup"),
                                login_link=url_for("login"))
    elif request.method == "POST":
        return signup_user(request.form.get("txtUser", default=None),
                           request.form.get("txtPass", default=None))

def signup_user(user, password):
    """
    Tries to sign the user up.
    """
    if user == None or password == None:
        return render_template("error.html.jinja", error="Invalid input")
    else:
        if database.nuevo_usuario(user, password):
            flash("New user created Succesfully.")
            return redirect(url_for("login"))
        else:
            flash("Error")
            return redirect(url_for("signup"))

@app.route("/home")
def home():
    """
    Displays the home page for logged in users. Otherwise redirects
    the request to login page.
    """
    user = session.get(USERNAME_KEY)
    if user == None:
        flash(f"Not logged in.")
        return redirect(url_for("login"))
    else:
        return render_template("home.html.jinja", username=user)

@app.route("/chat", methods=["POST"])
def chat():
    """
    Displays the chat page between the logged in user and a contact.
    If the user to chat with does not exist, redirects to home page.
    Otherwise redirects the request to login page.
    """
    if USERNAME_KEY not in session:
        flash("Not logged in.")
        return redirect(url_for("login"))
    
    contact = request.form.get("txtUser")
    if not database.exists_user(contact):
        flash(f"No se encontró el usuario {contact}")
        return redirect(url_for("home"))

    session[CHATWITH_KEY] = contact
    return render_template("chat.html.jinja", contact=contact)

@app.route("/messages")
def messages():
    """
    Returns a list of messages between the logged in user and a contact.
    If there is no contact, redirects to the home page.
    Otherwise redirects the request to login page.
    """
    if USERNAME_KEY not in session:
        flash(f"Not logged in.")
        return redirect(url_for("login"))

    if CHATWITH_KEY not in session:
        flash(f"Select a contacto to chat with")
        return redirect(url_for("home"))

    messages = database.get_mensajes(session[USERNAME_KEY],
                                     session[CHATWITH_KEY])
    message_list = []
    for message in messages:
        message_list.append(create_dictionary(message))
    return jsonify(message_list)

def create_dictionary(tuple):
    return {
        "sender" : tuple[0],
        "receiver" : tuple[1],
        "message" : tuple[2],
        "time" : tuple[3]
    }