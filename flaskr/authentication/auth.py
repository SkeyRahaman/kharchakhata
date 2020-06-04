from flask import Blueprint, redirect, render_template, request
from flaskr import app, db, bcrypt
from flaskr.functions import *
from flaskr.models import Users, Sex
from flaskr.forms import Login_form, RegistrationForm, Forgot_password_form, \
    Creat_new_password, Reset_password, Edit_profile_form
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer

bp = Blueprint('auth', __name__,
               template_folder='templates',
               static_folder='static')
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
email_link = URLSafeSerializer(app.config['SECRET_KEY'])


@bp.route("/login", methods=["get", 'post'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = Users.query.filter_by(email=request.form.get('email').lower()).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=request.form.get("remember"))
            session['user_name'] = user.fname
        else:
            flash("Email address and password does not match!.", "info")
        return redirect("/")
    else:
        return render_template("login.html", title="Login", form=form)


@bp.route('/registration_form', methods=['GET', 'POST'])
def registration_form():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        fname = request.form.get('fname').title()
        mname = request.form.get('mname').title()
        lname = request.form.get('lname').title()
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        sex = request.form.get("sex")
        new_user = Users(email=email, fname=fname,
                         mname=mname, lname=lname,
                         dob=dob, password=password,
                         phone=phone, sex=sex)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful!. Please Login with Your Email and Password!.", "success")
        token = email_link.dumps(email, salt="this_is_the_email")
        conform_url = "http://" + str(request.host) + "/conform_password/" + str(token)
        send_welcome_email(email=email, fname=fname, conform_url=conform_url)
        flash("A conformation Email is been send to your email address. Please verify your email address to use reset password functions.","info")
        return redirect("/")
    return render_template("register.html", title="Register", form=form)


@bp.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = Forgot_password_form()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        token = s.dumps(email, salt="this_is_the_email")
        reset_url = "http://" + str(request.host) + "/reset_password/" + str(token)
        send_mail(to=email, name=Users.query.filter_by(email=email).first().fname, reset_url=reset_url)
        flash("URL to reset your password is send to " + email + ", Visit your Email to Reset Your Password!",
              "success")
        return redirect('/')
    else:
        return render_template("forgot_password_one.html", form=form)


@bp.route('/conform_password/<token>')
def conform_password(token):
    email = email_link.loads(token, salt="this_is_the_email")
    b = Users.query.filter(Users.email == email).first()
    b.email_conformation = 1
    db.session.commit()
    flash("Email address conformed.!", "success")
    flash("Please login with your email and password if not loged in.", "info")
    return redirect("/")


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


@bp.route('/my_account', methods=['post', 'get'])
@login_required
def my_account():
    form = Edit_profile_form()
    form.setemail(email=current_user.email)
    if request.method == 'POST' and form.validate_on_submit():
        user = Users.query.filter_by(email=current_user.email).first()
        user.fname = request.form.get("fname").title()
        user.mname = request.form.get('mname').title()
        user.lname = request.form.get('lname').title()
        if current_user.email != request.form.get('email').lower():
            user.email = request.form.get('email').lower()
            user.email_conformation = 0
            flash("""You just Changed your email address.
            Prease conform your email address to use the reset passsword function!""", 'success')
        user.phone = request.form.get('phone')
        user.dob = request.form.get('dob')
        user.sex_id = request.form.get('sex')
        db.session.commit()
        flash("Change Saved Successfully.", 'success')
    return render_template('my_account.html',
                           title="My Account",
                           form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')