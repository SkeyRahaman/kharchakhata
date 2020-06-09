from flask import Blueprint, redirect, render_template, request
from flaskr import app, db, bcrypt, client
from flaskr.functions import *
from flaskr.models import Users, Sex
from flaskr.forms import Login_form, RegistrationForm, Forgot_password_form, \
    Creat_new_password, Reset_password, Edit_profile_form, Profile_picture_form
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer
import boto3
import json
import requests

bp = Blueprint('auth', __name__,
               template_folder='templates',
               static_folder='static')
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
email_link = URLSafeSerializer(app.config['SECRET_KEY'])


@bp.route("/google_login")
def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@bp.route("/google_login/callback")
def callback_google():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config["GOOGLE_CLIENT_ID"], app.config["GOOGLE_CLIENT_SECRET"]),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):

        try:
            email = userinfo_response.json()["email"]
        except:
            email = ""
        b = Users.query.filter_by(email=email).first()
        if b:
            flash("Loged in as " + b.fname, "success")
            if b.email_conformation == 0:
                try:
                    if userinfo_response.json()["email_verified"]:
                        b.email_conformation = 1
                except:
                    pass
            db.session.commit()
            login_user(b, remember=False)
        else:

            try:
                fname = userinfo_response.json()["given_name"]
            except:
                fname = ""
            try:
                lname = userinfo_response.json()["family_name"]
            except:
                lname = ""

            try:
                if userinfo_response.json()["email_verified"]:
                    email_verified = 1
                else:
                    email_verified = 0
            except:
                email_verified = 0
            try:
                picture = userinfo_response.json()["picture"]
            except:
                picture = None
            new_user = Users(
                fname=fname.title(),
                lname=lname.title(),
                picture=picture,
                email=email.lower(),
                email_conformation=email_verified,
                sex=4,
                password="External Website Verified."
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful!. Please Login with Your Email and Password!.", "success")
            if email_verified == "0":
                token = email_link.dumps(email, salt="this_is_the_email")
                conform_url = "https://" + str(request.host) + "/conform_email/" + str(token)
                send_welcome_email(email=email, fname=fname, conform_url=conform_url)
                flash(
                    "A conformation Email is been send to your email address. Please verify your email address to use reset password functions.",
                    "info")
            b = Users.query.filter_by(email=email).first()
            if b:
                flash("Account created and Logged in as " + b.fname, "success")
                send_welcome_email_for_conformed_emails(b.email, b.fname)
                login_user(new_user, remember=False)

            else:
                flash("Login Problem... Try after some time.", "danger")

    else:
        return "User email not available or not verified by Google.", 400

    return redirect("/")


@bp.route("/login", methods=["get", 'post'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = Users.query.filter_by(email=request.form.get('email').lower()).first()
        if user:
            if user.password == "External Website Verified.":
                flash("You have registered through google authentication. Please login with google.", "info")
            else:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user, remember=request.form.get("remember"))
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
        conform_url = "https://" + str(request.host) + "/conform_email/" + str(token)
        send_welcome_email(email=email, fname=fname, conform_url=conform_url)
        flash(
            "A conformation Email is been send to your email address. Please verify your email address to use reset password functions.",
            "info")
        return redirect("/")
    form.sex.default = 4
    form.process()
    return render_template("register.html", title="Register", form=form)


@bp.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = Forgot_password_form()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        token = s.dumps(email, salt="this_is_the_email")
        reset_url = "https://" + str(request.host) + "/reset_password/" + str(token)
        send_mail(to=email, name=Users.query.filter_by(email=email).first().fname, reset_url=reset_url)
        flash("URL to reset your password is send to " + email + ", Visit your Email to Reset Your Password!",
              "success")
        return redirect('/')
    else:
        return render_template("forgot_password_one.html", form=form)


@bp.route('/conform_email/<token>')
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


@bp.route('/change_dp', methods=['post', 'get'])
@login_required
def change_dp():
    form = Profile_picture_form()
    if request.method == 'POST' and form.validate_on_submit():
        s3 = boto3.resource('s3',
                            aws_access_key_id=app.config["ACCESS_ID"],
                            aws_secret_access_key=app.config["ACCESS_KEY"]
                            )
        key = "dp_" + str(current_user.id) + "." + request.files["dp"].filename.split(".")[-1]
        try:
            s3.Bucket("kharchakhata-files").put_object(Key=key, Body=request.files["dp"], ACL='public-read')
            user = Users.query.filter_by(email=current_user.email).first()
            user.picture = "https://s3-{}.amazonaws.com/{}/{}".format(
                app.config["S3_REGION"],
                app.config['S3_BUCKET_NAME'],
                key
            )
            db.session.commit()
            flash("Profile picture updated..", "success")
            return redirect("/my_account")
        except:
            flash("Cannot uplode file!.. Try after some time.!.", "danger")

    return render_template("profile_picture.html", form=form)


@bp.route('/remove_dp')
@login_required
def remove_dp():
    user = Users.query.filter_by(email=current_user.email).first()
    user.picture = None
    db.session.commit()
    return redirect("/my_account")


@bp.route('/my_account/send_mail', methods=['post', 'get'])
@login_required
def my_account_send_confirmation_mail():
    token = email_link.dumps(current_user.email, salt="this_is_the_email")
    conform_url = "https://" + str(request.host) + "/conform_email/" + str(token)
    send_welcome_email(email=current_user.email, fname=current_user.fname, conform_url=conform_url)
    flash(
        "A conformation Email is been send to your email address. Please verify your email address to use reset password functions.",
        "info")
    return redirect("/my_account")


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
