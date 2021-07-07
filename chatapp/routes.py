from flask import (request, url_for, render_template, redirect, flash, jsonify)
from werkzeug.urls import url_parse
from flask_login import (current_user, login_user, logout_user, login_required)
from chatapp import app, db
from chatapp.forms import LoginForm, RegistrationForm, EditProfileForm
from chatapp.models import User, Open_chat, Message
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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
    return render_template("baseform.html.jinja", title="Log in", form=form)


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
        register_user(form.username.data, form.password.data, form.email.data)
        flash("User registered successfully.")
        return redirect(url_for("login"))
    # GET request
    return render_template("baseform.html.jinja", title="Sign up", form=form)


def register_user(user, password, email):
    """
    Tries to sign the user up.
    """
    user = User(username=user, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html.jinja", user=user)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html.jinja", form=form)


@app.route("/home")
@login_required
def home():
    """
    Displays the home page for logged in users. Otherwise redirects
    the request to login page.
    """
    open_chats = Open_chat.query.filter(
        db.or_(Open_chat.user1 == current_user,
               Open_chat.user2 == current_user)).all()
    return render_template("home.html.jinja", chats=open_chats)


@app.route("/chat/<username>")
@login_required
def chat(username):
    """
    Displays the chat page between the logged in user and a contact.
    If the user to chat with does not exist, raise 404 page.
    Otherwise redirects the request to login page.
    """
    # Check if the user we are trying to chat with exists.
    user = User.query.filter_by(username=username).first_or_404()
    # Check if there is an open chat with that user already
    # open_chat = Open_chat.query.filter(
    #     db.or_(
    #         db.and_(Open_chat.user1 == current_user, Open_chat.user2 == user),
    #         db.and_(Open_chat.user1 == user,
    #                 Open_chat.user2 == current_user))).first()
    # if open_chat is None:
    #     # Save the open chat
    #     open_chat = Open_chat(user1=current_user, user2=user)
    #     db.session.add(open_chat)
    #     db.session.commit()
    return render_template("chat.html.jinja", contact=user.username)


@app.route("/messages/<username>")
@login_required
def messages(username):
    """
    Returns a list of messages between the logged in user and a contact.
    If the user does not exists, raise 404.
    If there are no messages, redirects to the chat page.
    If the user is not logged in, redirects the request to login page.
    """
    # Check if the user exists.
    user = User.query.filter_by(username=username).first_or_404()
    # Check if there is an open chat with that user already
    open_chat = Open_chat.query.filter(
        db.or_(
            db.and_(Open_chat.user1 == current_user, Open_chat.user2 == user),
            db.and_(Open_chat.user1 == user,
                    Open_chat.user2 == current_user))).first()
    if open_chat is None:
        # Redirect to home.
        flash("There are no messages.")
        return redirect(url_for("chat", username=user.username))
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.from_user == current_user,
                    Message.to_user == user),
            db.and_(Message.from_user == user,
                    Message.to_user == current_user))).all()
    message_list = []
    for message in messages:
        message_list.append(create_dictionary(message))
    return jsonify(message_list)


def create_dictionary(message):
    return {
        "sender": message.from_user.username,
        "receiver": message.to_user.username,
        "message": message.body,
        "time": message.timestamp
    }


@app.route("/sendMessage/<username>", methods=["POST"])
@login_required
def send_message(username):
    """
    Sends a message from the logged user to a contact.
    If there is no contact, redirects to the chat page.
    """
    # Check if the user exists.
    user = User.query.filter_by(username=username).first_or_404()
    # Get the body of the message to send.
    msg = request.form.get("txtMessage", default=None)
    if msg is None:
        flash("No Message.")
        return redirect(url_for("chat", username=user.username))
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
        db.session.commit()
    # Save the message
    new_msg = Message(from_user=current_user, to_user=user, body=msg)
    db.session.add(new_msg)
    db.session.commit()
    return {"status": "ok"}
