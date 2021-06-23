from flask import (
    request, url_for, render_template, redirect,
    abort, session, flash, jsonify
)
from werkzeug.urls import url_parse
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from chatapp import app, db
from chatapp.forms import LoginForm, RegistrationForm
from chatapp.models import User

USERNAME_KEY = "logged_user"
CHATWITH_KEY = "chat"

@app.route('/')
@app.route("/index")
def index():
    """
    Displays index page.
    If the user has an active session it redirects the request to home.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return render_template('index.html.jinja')

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Displays login page if it's a GET request.
    Tries to log user in if it's a POST request.
    """
    # if the user navigates to /login but is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    # POST request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))
        # Login valid
        login_user(user, remember=form.remember_me.data)
        flash(f"Successufully logged in as {user.username}", "message")
        # Redirects to next page
        next_page = request.args.get('next')
        # Check if next page is null or is a full URL
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    # GET request
    return render_template("baseform.html.jinja", 
                                title="Log in",
                                form=form)

@app.route("/logout")
def logout():
    """
    Terminates the user session and redirects to index.
    """
    logout_user()
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Displays signup page if it's a GET request.
    Tries to register the user if it's a POST request.
    """
    # if the user navigates to /signup or /register 
    # but is already logged in.
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # POST request
        register_user(
            form.username.data, form.password.data, form.email.data)
        flash("User registered successfully.")
        return redirect(url_for("login"))
    # GET request
    return render_template("baseform.html.jinja",
                            title="Sign up",
                            form=form)

def register_user(user, password, email):
    """
    Tries to sign the user up.
    """
    user = User(username=user, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
@app.route("/home")
@login_required
def home():
    """
    Displays the home page for logged in users. Otherwise redirects
    the request to login page.
    """
    user = current_user
    return render_template("home.html.jinja")

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    """
    Displays the chat page between the logged in user and a contact.
    If the user to chat with does not exist, redirects to home page.
    Otherwise redirects the request to login page.
    """
    # Create new form in forms module
    contact = request.form.get("txtUser")
    if not database.exists_user(contact):
        flash(f"No se encontró el usuario {contact}")
        return redirect(url_for("home"))

    session[CHATWITH_KEY] = contact
    return render_template("chat.html.jinja", contact=contact)

@app.route("/messages")
@login_required
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
        flash(f"Select a contact to chat with")
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

@app.route("/sendMessage", methods=["POST"])
@login_required
def send_message():
    """
    Sends a message from the logged user to a contact.
    If there is no contact, redirects to the home page.
    """
    if USERNAME_KEY not in session:
        flash(f"Not logged in.")
        return redirect(url_for("login"))

    if CHATWITH_KEY not in session:
        flash(f"Select a contacto to chat with")
        return redirect(url_for("home"))
    
    msg = request.form.get("txtMessage", default = None)
    if msg is None:
        flash(f"No message.")
        return redirect(url_for("chat"))

    database.crear_mensaje(session[USERNAME_KEY], 
                           session[CHATWITH_KEY],
                           msg)

    return {"status": "ok"}