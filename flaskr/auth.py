from flaskr.functions import *
from flask import (Blueprint, redirect, render_template, request, session, jsonify)
from itsdangerous import URLSafeTimedSerializer
from flaskr.forms import RegistrationForm,Forgot_password_form

bp = Blueprint('auth', __name__)  # url_prefix="/auth"

s = URLSafeTimedSerializer(session)


@bp.route("/login_validation", methods=['post'])
def login_validation():
    if str(request.form.get("remember")) == "on":
        session.permanent = True
    email = request.form.get('email').lower()
    password = request.form.get('password')
    login_with(email=email, password=password)
    return redirect("/")


@bp.route('/registration_form', methods=['GET', 'POST'])
def registration_form():
    return render_template("/register.html", title="Register", form=RegistrationForm())


@bp.route('/admin_login_validation', methods=['post'])
def admin_login_validation():
    if str(request.form.get("remember_me")) == "on":
        session.permanent = True
    email = request.form.get('email').lower()
    password = request.form.get('password')
    login_with_for_admin(email=email, password=password)
    return redirect("/admin")


@bp.route("/register_user", methods=['post'])
def register_user():
    fname = request.form.get('fname').title()
    mname = request.form.get('mname').title()
    lname = request.form.get('lname').title()
    remail = request.form.get('remail').lower()
    phone = request.form.get('rphone')
    dob = request.form.get('dob')
    sex = request.form.get('sex')
    sex = (run_in_database("""SELECT * FROM `sex` WHERE `type` LIKE '{}'""".format(sex), fetch='yes'))[0][0]
    password = request.form.get('password')

    quary = """INSERT INTO `users`(`fname`,`mname`,`lname`,`dob`,`sex_id`,`phone`,`email`,`password`) VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(
        fname,
        mname,
        lname,
        dob, sex, phone,
        remail,
        password)
    result = run_in_database(quary=quary, commit='yes')
    if result:
        login_with(email=remail, password=password)
        return redirect('/dashboard/all/all')


@bp.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@bp.route('/forgot_password')
def forgot_password():
    return render_template("forgot_password_one.html", form=Forgot_password_form())


@bp.route('/forgot_password_last', methods=['post'])
def forgot_password_last():
    email = request.form.get('email').lower()
    token = s.dumps(email, salt="this_is_the_email")
    reset_url = "http://" + str(request.host) + "/reset_password/" + str(token)
    if email != "":
        query = """SELECT `user_id`,`fname` FROM `users` WHERE `users`.`email` LIKE '{}'""".format(email)
        result = run_in_database(quary=query, fetch='yes')
        if len(result) != 0:
            send_mail(to=email, name=result[0][1], reset_url=reset_url)
            return redirect('/')
        else:
            return redirect('/forgot_password')
    else:
        return redirect('/forgot_password')


@bp.route('/reset_password/<token>')
def reset_password_with_token(token):
    email = s.loads(token, salt="this_is_the_email", max_age=3600)
    query = """SELECT `user_id`,`fname` FROM `users` WHERE `users`.`email` LIKE '{}'""".format(email)
    result = run_in_database(quary=query, fetch='yes')
    return render_template("reset_password.html", user_id=result[0][0], user_name=result[0][1], token=token)


@bp.route('/reset_password_final/<token>', methods=['post'])
def reset_password_final(token):
    try:
        email = s.loads(token, salt="this_is_the_email", max_age=3600)
        password = request.form.get('cnpassword')
        query = "UPDATE `users` SET `password`= '{}' WHERE `email` = '{}';".format(password, email)
        _ = run_in_database(quary=query, commit='yes')
        return redirect("/")
    except:
        return redirect("/")


@bp.route('/password_validation', methods=['post'])
def password_validation():
    cpassword = request.form.get('cpassword')
    npassword = request.form.get('npassword')
    cnpassword = request.form.get('cnpassword')

    query = """SELECT `password` FROM `users` WHERE `user_id` LIKE {};""".format(session['user_id'])
    current_password = run_in_database(quary=query, fetch='yes')
    if not current_password:
        return redirect('/settings/"Internal error!!"')
    else:
        current_password = current_password[0][0]

    if (current_password == cpassword) and (npassword == cnpassword):
        query = """UPDATE `users` SET `password`= '{}' WHERE `user_id` LIKE {};""".format(cnpassword,
                                                                                          session['user_id'])
        __ = run_in_database(quary=query, commit='yes')
        return redirect('/dashboard/all/all')
    elif (current_password != cpassword) and (npassword == cnpassword) and (len(npassword) > 3):
        return redirect('/settings/"Wrong Current Password"')
    else:
        return redirect('/settings/none')


@bp.route('/check_email_address/<email>')
def check_email_address(email):
    query = "SELECT * FROM `users` WHERE `users`.`email` LIKE '{}';".format(email)
    result = run_in_database(quary=query, fetch='yes')
    if len(result) != 0:
        return jsonify(True)
    else:
        return jsonify(False)


@bp.route('/admin')
def admin():
    if 'admin_user_id' in session:
        query = "SELECT * FROM `type` WHERE `active` LIKE 1 ORDER BY `type`;"
        type = run_in_database(quary=query, fetch='yes')
        query = "SELECT * FROM `sub_type` ORDER BY `subtype`;"
        sub_type = run_in_database(quary=query, fetch='yes')
        query = """SELECT `type_sub_type`.`type_sub_type_id`,`type_sub_type`.`type_id`,`type`.`type`,`type_sub_type`.`sub_type_id`,`sub_type`.`subtype` FROM `type_sub_type` 

    JOIN `type` ON 
    `type_sub_type`.`type_id` = `type`.`type_id` 

    JOIN `sub_type` ON
    `type_sub_type`.`sub_type_id` = `sub_type`.`sub_type_id` ORDER BY `type`.`type` ASC , `sub_type`.`subtype` ASC;"""
        type_sub_type_table = run_in_database(quary=query, fetch='yes')
        return render_template("admin.html", type=type, sub_type=sub_type, type_sub_type_t=type_sub_type_table,
                               user_name=session['admin_name'])
    else:
        return redirect('/admin_login')


@bp.route('/admin_login')
def admin_login():
    return render_template("admin_login.html")
