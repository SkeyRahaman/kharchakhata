from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, jsonify)
from flaskr.functions import *
from datetime import datetime as dt
from flaskr.forms import Login_form, RegistrationForm

bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route('/')
def home():
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


@bp.route('/admin_login_validation', methods=['post'])
def admin_login_validation():
    if str(request.form.get("remember_me")) == "on":
        session.permanent = True
    email = request.form.get('email').lower()
    password = request.form.get('password')
    login_with_for_admin(email=email, password=password)
    return redirect("/admin")


@bp.route('/admin_login')
def admin_login():
    return render_template("admin_login.html")
