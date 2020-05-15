from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TimeField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from flaskr.models import Users


class Forgot_password_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Mail')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email Address not registered!. You can Register as new User!.")


class Reset_password(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    npassword = PasswordField('New Password',
                              validators=[DataRequired()])
    cnpassword = PasswordField('Confirm New Password',
                               validators=[DataRequired(), EqualTo('npassword')])
    submit = SubmitField("Change Password.")


class Creat_new_password(FlaskForm):
    npassword = PasswordField('Password',
                              validators=[DataRequired()])
    cnpassword = PasswordField('Confirm Password',
                               validators=[DataRequired(), EqualTo('npassword')])
    submit = SubmitField('Sign Up')


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[
                            DataRequired(),
                            Length(min=2, max=20)
                        ])
    mname = StringField('Middle Name')
    lname = StringField('Last Name',
                        validators=[
                            DataRequired(),
                            Length(min=2, max=20)
                        ])

    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=20)])
    cpassword = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already registered with username as ' + user.fname)


class Login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email Address not registered!. You can Register as new User!.")
