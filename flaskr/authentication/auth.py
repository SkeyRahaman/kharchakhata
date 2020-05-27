from flask import Blueprint, redirect, render_template, request
from flaskr import app, db, bcrypt
from flaskr.functions import *
from flaskr.models import Users, Sex
from flaskr.forms import Login_form, RegistrationForm, Forgot_password_form, Creat_new_password, Reset_password
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer

bp = Blueprint('auth', __name__,
               template_folder='templates',
               static_folder='static')  # url_prefix="/auth"
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])


@bp.route("/login", methods=["get", 'post'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = Users.query.filter_by(email=request.form.get('email').lower()).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=request.form.get("remember"))
            session['user_name'] = user.fname
            # app = create_dashboard()
        else:
            flash("Email address and password does not match!.", "info")
        return redirect("/")
    else:
        return render_template("login.html", title="Login", form=form)


@bp.route('/registration_form', methods=['GET', 'POST'])
def registration_form():
    form = RegistrationForm()
    form.sex.choices = [(str(sex.id), sex.type) for sex in Sex.query.all()]
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        fname = request.form.get('fname').title()
        mname = request.form.get('mname').title()
        lname = request.form.get('lname').title()
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        new_user = Users(email=email, fname=fname,
                         mname=mname, lname=lname,
                         dob=dob, password=password,
                         phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration Successful!. Please Login with Your Email and Password!.", "success")
        return redirect("/")
    return render_template("register.html", title="Register", form=form)


@bp.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = Forgot_password_form()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        token = s.dumps(email, salt="this_is_the_email")
        reset_url = "http://" + str(request.host) + "/reset_password/" + str(token)
        print(reset_url)
        #send_mail(to=email, name=Users.query.filter_by(email=email).first().fname, reset_url=reset_url)
        flash("URL to reset your password is send to " + email + ", Visit your Email to Reset Your Password!",
              "success")
        return redirect('/')
    else:
        return render_template("forgot_password_one.html", form=form)


@bp.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password_with_token(token):
    form = Creat_new_password()
    try:
        email = s.loads(token, salt="this_is_the_email", max_age=900)
    except:
        flash("URL for password reset Expired!. Try Password reset option again to get a valid Password Reset URL.",
              "danger")
        return redirect("/")
    if form.validate_on_submit():
        user = Users.query.filter_by(email=email).first()
        user.password = bcrypt.generate_password_hash(request.form.get('cnpassword')).decode('utf-8')
        db.session.commit()
        flash("Password Changed Successfully!. Try Login with new Password.", "success")
        return redirect("/")
    else:
        return render_template("reset_password.html", form=form, )


@bp.route('/my_account')
@login_required
def my_account(): 
    return render_template('my_account.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
