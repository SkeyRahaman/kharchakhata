from flask_wtf import FlaskForm
from wtforms_components import TimeField
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, FloatField, TextAreaField, \
    IntegerField, FileField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, optional
from flask_wtf.file import FileAllowed, FileRequired
from flaskr.models import Users, Sex
from flask import flash


class Expence_form(FlaskForm):
    name = StringField("Expence Name", validators=[Length(min=3, max=20)])
    date = DateField("Date", validators=[DataRequired()])
    today = BooleanField("Today")
    time = TimeField('Time', validators=[DataRequired()])
    now = BooleanField("Now")
    type = SelectField("Type", choices=[], validate_choice=False)
    subtype = SelectField("Subtype", choices=[], validate_choice=False)
    frequency = SelectField("Frequency", choices=[], validate_choice=False)
    payment_method = SelectField("Payment Method", choices=[], validate_choice=False)
    transaction_type = SelectField("Transaction Type", choices=[("1", "Debit"), ("2", "Credit")])
    amount = FloatField("Amount")
    comment = TextAreaField('Comment', render_kw={"rows": 5, "cols": 11, "placeholder": "Under 90 character"},
                            validators=[Length(max=95)])

    submit = SubmitField("Save")


class Forgot_password_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Mail')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email Address not registered!. You can Register as new User!.")
        if user.email_conformation == 0:
            flash("You can conform your email address from The conformation mail that we send you.", "info")
            raise ValidationError("Email Address not conformed!!.")


class Reset_password(FlaskForm):
    password = PasswordField('Password')
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


class Profile_picture_form(FlaskForm):
    dp = FileField('profile picture',
                   validators=[
                       FileRequired(),
                       FileAllowed(['jpg', 'png'], 'Images only!')
                   ])
    submit = SubmitField("Change!")


class Edit_profile_form(FlaskForm):
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
    sex = SelectField("Gender", choices=[(str(sex.id), sex.type) for sex in Sex.query.all()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField("Date of Birth", validators=[optional()])
    phone = StringField("Phone Number (Along with country code).", validators=[Length(max=14)])
    submit = SubmitField('Sign Up')
    current_email = None

    def setemail(self, email=None):
        self.current_email = email

    def validate_email(self, email):
        if self.current_email != email.data:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address already registered with username as ' + user.fname)


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
    sex = SelectField("Gender", choices=[(str(sex.id), sex.type) for sex in Sex.query.all()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField("Date of Birth", validators=[optional()])
    phone = StringField("Phone Number (Along with country code).", validators=[Length(max=14)])
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
