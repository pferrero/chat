from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class LoginForm(SignupForm):    
    remember_me = BooleanField("Remember me")