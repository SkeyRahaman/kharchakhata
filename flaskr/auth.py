from flaskr.functions import *
from flask import (Blueprint, redirect, render_template, request, session)
from flaskr.forms import Login_form, RegistrationForm, Forgot_password_form, Creat_new_password,Reset_password
from itsdangerous import URLSafeTimedSerializer

bp = Blueprint('auth', __name__)  # url_prefix="/auth"

s = URLSafeTimedSerializer("Very secret key")


@bp.route("/login", methods=["get", 'post'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        if str(request.form.get("remember")) == "on":
            session.permanent = True
        email = request.form.get('email').lower()
        password = request.form.get('password')
        login_with(email=email, password=password)
        return redirect("/")
    else:
        return render_template("login.html", title="Login", form=form)


@bp.route('/registration_form', methods=['GET', 'POST'])
def registration_form():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        fname, email = check_email_in_databace(email)
        if not email:
            fname = request.form.get('fname').title()
            mname = request.form.get('mname').title()
            lname = request.form.get('lname').title()
            dob = request.form.get('dob')
            password = request.form.get('password')
            quary = """INSERT INTO `users`(`fname`,`mname`,`lname`,`dob`,`email`,`password`) VALUES('{}','{}','{}','{}','{}',{})""".format(
                fname,
                mname,
                lname,
                dob, email,
                password)
            try:
                result = run_in_database(quary=quary, commit='yes')
            except:
                result = False
            if result:
                login_with(email=email, password=password)
                return redirect("/")
        else:
            flash("Email address already registered with username as " + fname + "!.", "danger")
            return redirect("/")
    return render_template("register.html", title="Register", form=form)


@bp.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = Forgot_password_form()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        name, email = check_email_in_databace(email)
        if name:
            token = s.dumps(email, salt="this_is_the_email")
            reset_url = "http://" + str(request.host) + "/reset_password/" + str(token)
            print(reset_url)
            # send_mail(to=email, name=name, reset_url=reset_url)
            flash("URL to reset your password is send to " + email + ", Visit your Email to Reset Your Password!",
                  "success")
            return redirect('/')
        else:
            flash("Email Address Not Registered!", "danger")
            redirect("/")
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
        password = request.form.get('cnpassword')
        query = "UPDATE `users` SET `password`= '{}' WHERE `email` = '{}';".format(password, email)
        _ = run_in_database(quary=query, commit='yes')
        flash("Password Changed Successfully!. Try Login with new Password.", "success")
        return redirect("/")
    else:
        return render_template("reset_password.html", form=form, )


@bp.route('/password_validation', methods=['GET', 'POST'])
def password_validation():
    form = Reset_password()
    if form.validate_on_submit():
        cpassword = request.form.get('password')
        cnpassword = request.form.get('cnpassword')

        query = """SELECT `password` FROM `users` WHERE `user_id` LIKE {};""".format(session['user_id'])
        current_password = run_in_database(quary=query, fetch='yes')
        current_password = current_password[0][0]

        if current_password == cpassword:
            query = """UPDATE `users` SET `password`= '{}' WHERE `user_id` LIKE {};""".format(cnpassword,
                                                                                              session['user_id'])
            __ = run_in_database(quary=query, commit='yes')
            flash("Password Updated Successful!.", "success")
        else:
            flash("Current Password Does Not Match!", "danger")
    return redirect("/settings")


@bp.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('name')
    return redirect('/')