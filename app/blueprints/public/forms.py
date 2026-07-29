# app/blueprints/public/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

from app.models import MEETING_PLATFORM_CHOICES, SERVICE_CHOICES


class WorkWithKonvexityForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(message="Please enter your full name."), Length(max=200)],
    )
    email = StringField(
        "Email Address",
        validators=[DataRequired(message="Please enter your email."), Email(message="Enter a valid email."), Length(max=300)],
    )
    whatsapp_number = StringField(
        "WhatsApp Number",
        validators=[DataRequired(message="Please enter your WhatsApp number."), Length(max=50)],
    )
    company = StringField("Company / Organization", validators=[Optional(), Length(max=300)])
    job_title = StringField("Job Title", validators=[Optional(), Length(max=200)])
    country = StringField("Country", validators=[Optional(), Length(max=100)])

    service_interest = SelectField(
        "What do you need?",
        choices=SERVICE_CHOICES,
        validators=[DataRequired(message="Please select a service.")],
    )
    message = TextAreaField(
        "Tell us about your project",
        validators=[Optional(), Length(max=4000)],
    )

    submit = SubmitField("Submit Request")


class ScheduleConsultationForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(message="Please enter your full name."), Length(max=200)],
    )
    email = StringField(
        "Email Address",
        validators=[DataRequired(message="Please enter your email."), Email(message="Enter a valid email."), Length(max=300)],
    )
    whatsapp_number = StringField(
        "WhatsApp Number",
        validators=[DataRequired(message="Please enter your WhatsApp number."), Length(max=50)],
    )
    company = StringField("Company / Organization", validators=[Optional(), Length(max=300)])

    meeting_goal = TextAreaField(
        "What would you like to discuss?",
        validators=[Optional(), Length(max=2000)],
    )
    preferred_platform = SelectField(
        "Preferred Platform",
        choices=MEETING_PLATFORM_CHOICES,
        validators=[DataRequired(message="Please choose a platform.")],
    )
    preferred_date = StringField(
        "Preferred Date",
        validators=[DataRequired(message="Please share a preferred date.")],
    )
    preferred_time = StringField(
        "Preferred Time",
        validators=[DataRequired(message="Please share a preferred time.")],
    )

    submit = SubmitField("Request Consultation")