from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, jsonify)
from flaskr.functions import *
from flask_login import login_required
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


@bp.route('/add_to_table/<table>/<value>')
@login_required
def add_to_type(table, value):
    if 'admin_user_id' in session:
        if table == "type":
            col_name = "type"
        else:
            col_name = "subtype"
        query = "SELECT * FROM `{}` WHERE `{}` LIKE '{}';".format(table, col_name, value.title())
        present = run_in_database(quary=query, fetch='yes')
        if not present:
            query = "INSERT INTO `{}`(`{}`) VALUES ('{}');".format(table, col_name, value.title())
            __ = run_in_database(quary=query, commit='yes')
            print(True)
            return jsonify(True)
        else:
            print(False)
            return jsonify(False)
    else:
        return redirect('/admin_login')


@bp.route('/add_relation/<type_id>/<sub_type_id>')
@login_required
def add_relation(type_id, sub_type_id):
    if 'admin_user_id' in session:
        query = "SELECT `type_id` FROM `type` WHERE `type_id` LIKE {}".format(type_id)
        result = run_in_database(quary=query, fetch='yes')
        print(result)
        if result:
            query = "SELECT `sub_type_id` FROM `sub_type` WHERE `sub_type_id` LIKE {}".format(sub_type_id)
            result = run_in_database(quary=query, fetch='yes')
            if result:
                query = """SELECT `type_sub_type_id` FROM `type_sub_type` WHERE `type_id` LIKE {} AND `sub_type_id` LIKE {};""".format(
                    type_id, sub_type_id)
                result = run_in_database(quary=query, fetch='yes')
                if not result:
                    query = "INSERT INTO `type_sub_type`(`type_id`,`sub_type_id`) VALUES ({},{})".format(type_id,
                                                                                                         sub_type_id)
                    _ = run_in_database(quary=query, commit='yes')
                    return jsonify(True)
                else:
                    return jsonify("This Relation is already Present!.")
            else:
                return jsonify(False)
        else:
            return jsonify(False)
    else:
        return redirect('/admin_login')


@bp.route('/update_relation_table_in_admin_page/<type_id>/<sub_type_id>')
@login_required
def update_relation_table_in_admin_page(type_id, sub_type_id):
    if 'admin_user_id' in session:
        if type_id != "all":
            start = "WHERE"
            type_filter = " `type_sub_type`.`type_id` LIKE {} ".format(type_id)
            mid = "AND"
        else:
            start = ""
            type_filter = ""
            mid = ""

        if sub_type_id != "all":
            start = "WHERE"
            sub_type_filter = " `type_sub_type`.`sub_type_id` LIKE {} ".format(sub_type_id)
        else:
            mid = ""
            sub_type_filter = ""

        query = """SELECT `type_sub_type`.`type_sub_type_id`,`type_sub_type`.`type_id`,`type`.`type`,`type_sub_type`.`sub_type_id`,`sub_type`.`subtype` FROM `type_sub_type` 

        JOIN `type` ON 
        `type_sub_type`.`type_id` = `type`.`type_id` 

        JOIN `sub_type` ON
         `type_sub_type`.`sub_type_id` = `sub_type`.`sub_type_id` """ + start + type_filter + mid + sub_type_filter + " ORDER BY `type`.`type` ASC , `sub_type`.`subtype` ASC;"
        result = run_in_database(quary=query, fetch='yes')
        return jsonify(result)
    else:
        return redirect('/admin_login')


@bp.route('/delete_relation_table/<relation_id>')
@login_required
def delete_relation_table(relation_id):
    if 'admin_user_id' in session:
        try:
            query = """DELETE FROM `type_sub_type` WHERE `type_sub_type`.`type_sub_type_id` LIKE {} ;""".format(
                relation_id)
            __ = run_in_database(quary=query, commit='yes')
            return jsonify(True)
        except:
            return jsonify(False)
    else:
        return redirect('/admin_login')
