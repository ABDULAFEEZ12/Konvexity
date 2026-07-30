# app/blueprints/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired(message="Enter your current password.")],
    )
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(message="Enter a new password."), Length(min=8, max=200, message="Password must be at least 8 characters.")],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(message="Confirm your new password."), EqualTo("new_password", message="Passwords do not match.")],
    )
    submit = SubmitField("Update Password")
