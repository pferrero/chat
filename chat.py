from flask import Flask, request, url_for, render_template, redirect, abort, session, flash
import database

USERNAME_KEY = "logged_user"

app = Flask(__name__)
app.secret_key = b'8B\x89f\xf0\x89\xa0\xfb\xdb+\xacDma\xb9?'

@app.route('/')
def index():
    """
    Displays index page.
    """
    return render_template('index.html.jinja',
                            signup_link=url_for("signup"),
                            login_link=url_for("login"))

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
        login = database.verificar_usuario(username, password)
        if login:
            session[USERNAME_KEY] = username
            flash(f"Successufully logged in as {username}")
            return redirect(url_for("home"))
        else:
            flash(f"Invalid user or password")
            return redirect(url_for("login"))

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
            return "Usuario creado"
        else:
            return "Usuario existente"

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
        return f"Welcome {user}"