from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TimeField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class Forgot_password_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Mail')


class Reset_password(FlaskForm):
    npassword = PasswordField('Password',
                              validators=[DataRequired()])
    cnpassword = PasswordField('Confirm Password',
                               validators=[DataRequired(), EqualTo(npassword)])
    submit = SubmitField('Sign Up')


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[
                            DataRequired(),
                            Length(min=3, max=20)
                        ])

    mname = StringField('Middle Name',
                        validators=[
                            DataRequired(),
                            Length(min=3, max=20)
                        ])

    lname = StringField('Last Name',
                        validators=[
                            DataRequired(),
                            Length(min=3, max=20)
                        ])

    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    cpassword = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Sign Up')


class Login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
