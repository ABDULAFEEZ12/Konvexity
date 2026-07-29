# app/blueprints/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class AdminLoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(message="Email is required."), Email(message="Enter a valid email."), Length(max=300)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required."), Length(min=8, max=200)],
    )
    remember = BooleanField("Keep me signed in")
    submit = SubmitField("Sign In")