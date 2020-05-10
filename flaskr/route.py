from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, jsonify)
from flaskr.functions import *
from datetime import datetime as dt
from flaskr.forms import Login_form, RegistrationForm
bp = Blueprint('route', __name__)


@bp.route("/")
def home():
    if 'user_id' not in session:
        flash("Done", "success")
        return render_template('login.html', form=Login_form())
    elif 'user_id' in session:
        month = datetime.now().strftime("%B")
        year = datetime.now().year
        return redirect("/dashboard/{}/{}".format(month, year))


@bp.route("/enter_transaction", methods=['post'])
def enter_transaction():
    entry = 1

    # print(date_check == None , time_check == "on")
    expence_name = request.form.get("ex_name").title()
    date_check = request.form.get("today_check")
    if date_check is None:
        date = request.form.get("transaction_date")
    else:
        date = dt.today()
    amount = request.form.get("amount")
    time_check = request.form.get("time_check")
    if time_check is None:
        time = request.form.get("transaction_time")
    else:
        time = datetime.now().strftime('%H:%M:%S')
    user_id = session['user_id']
    credit_debit = request.form.get("credit_debit")
    type_ = request.form.get("type")
    sub_type = request.form.get("sub_type")
    frequency = request.form.get("frequency")
    payment_method = request.form.get("pay_method")
    query = """INSERT INTO `expences` 
            (`expence_name`,`date`,`amount`,`time`,`user_id`,`credit_debit_id`,`type_id`,`sub_type_id`,`frequency_id`,`payment_medium_id`)
             VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(expence_name, date, amount, time,
                                                                                 user_id, credit_debit, type_,
                                                                                 sub_type, frequency, payment_method)
    __ = run_in_database(quary=query, commit='yes')

    if entry == 1:
        return redirect('/')


@bp.route('/dashboard/<string:month>/<string:year>')
def dashboard(month, year):
    if month == 'all' and year == 'all':
        month_filter = ""
    else:
        month_filter = """AND MONTH(date) = {}  AND YEAR(date) = {} """.format(datetime.strptime(month, '%B').month,
                                                                               year)
    interval = {'month': month, 'year': year}
    if 'user_id' in session:
        type_ = run_in_database(quary="SELECT * FROM `type` WHERE `active` LIKE 1 ORDER BY `type` ", fetch='yes')
        type_list = []
        for i in type_:
            type_list.append([i[0], i[1]])
        sub_type = run_in_database(quary="SELECT * FROM `sub_type` WHERE `active` LIKE 1 ORDER BY `subtype`",
                                   fetch='yes')
        sub_type_list = []
        for i in sub_type:
            sub_type_list.append([i[0], i[1]])
        frequency_items = run_in_database(quary="SELECT * FROM `frequency` WHERE `active` LIKE 1 ORDER BY `type`",
                                          fetch='yes')
        payment_mediums = run_in_database(quary="SELECT * FROM `payment_medium` WHERE `active` LIKE 1 ORDER BY `type`",
                                          fetch='yes')

        query = """SELECT `expences`.`expence_name`,`expences`.`date`,`expences`.`time`,`credit_debit`.`type`,`type`.`type`,`sub_type`.`subtype`,`frequency`.`type`,`expences`.`amount`,`payment_medium`.`type`, `expences`.`expence_id` FROM 
            `expences` 

            JOIN `credit_debit` ON 
            `expences`.`credit_debit_id` = `credit_debit`.`credit_debit_id`

            JOIN `type` ON 
            `expences`.`type_id` = `type`.`type_id`

            JOIN `sub_type` ON
            `expences`.`sub_type_id` = `sub_type`.`sub_type_id`

            JOIN `frequency` ON
            `expences`.`frequency_id` = `frequency`.`frequency_id`

            JOIN `payment_medium` ON
            `expences`.`payment_medium_id` = `payment_medium`.`medium_id`

            WHERE `expences`.`user_id` = {} {}

            ORDER BY `expences`.`date` DESC , `expences`.`time` DESC LIMIT 10 """.format(session['user_id'],
                                                                                         month_filter)
        table_data = run_in_database(query, fetch='yes')

        query = (
                """SELECT SUM(`expences`.`amount`) FROM `expences` WHERE `expences`.`credit_debit_id` LIKE 1 AND `expences`.`user_id` LIKE '{}'""" + month_filter).format(
            session['user_id'])
        total_income = run_in_database(quary=query, fetch='yes')[0][0]
        if total_income is None:
            total_income = 0
        query = (
                """SELECT SUM(`expences`.`amount`) FROM `expences` WHERE `expences`.`credit_debit_id` LIKE 2 AND `expences`.`user_id` LIKE '{}'""" + month_filter).format(
            session['user_id'])
        total_expence = run_in_database(quary=query, fetch='yes')[0][0]
        if total_expence is None:
            total_expence = 0
        total_savings = total_income - total_expence
        average_saving_per_month_upto_this_date = 12000
        last_month_last_date = dt.today().replace(day=1) - timedelta(days=1)
        last_month_first_day = last_month_last_date.replace(day=1)
        query = """SELECT SUM(`expences`.`amount`) FROM `expences` WHERE `expences`.`credit_debit_id` LIKE 1 AND `expences`.`user_id` LIKE '{}' AND `expences`.`date` < '{}' AND `expences`.`date` > '{}' """.format(
            session['user_id'], last_month_last_date, last_month_first_day)

        last_month_savings = run_in_database(query, fetch='yes')[0][0]
        nav_bar = {'income': total_income, 'expence': total_expence, 'savings': total_savings,
                   'avg': average_saving_per_month_upto_this_date,
                   'last_month_savings': last_month_savings}

        query = """SELECT DISTINCT MONTH(date),YEAR(date) FROM `expences` WHERE `expences`.`user_id` LIKE '{}'""".format(
            session['user_id'])
        months = run_in_database(quary=query, fetch='yes')
        month = []
        year = []
        for i in months:
            month.append(i[0])
            year.append(i[1])
        months = []
        for i in range(len(month)):
            months.append([calendar.month_name[month[i]], year[i]])

        return render_template('dashboard.html', user_name=session['name'],
                               type_list=type_list,
                               sub_type_list=sub_type_list,
                               frequency=frequency_items,
                               payment_medium=payment_mediums,
                               table=table_data,
                               nav_bar=nav_bar,
                               months=months,
                               interval=interval)
    else:
        return redirect('/')


@bp.route('/my_account')
def my_account():
    query = """SELECT `users`.`fname` , `users`.`mname`, `users`.`lname` ,`users`.`dob`,`users`.`email`,
    `users`.`phone`,`sex`.`type`,`users`.`sex_id` FROM `users` JOIN `sex` ON `users`.`sex_id` = `sex`.`sex_id` WHERE `users`.`user_id` = {}""".format(
        session['user_id'])
    user_details = run_in_database(quary=query, fetch='yes')[0]
    return render_template('my_account.html', user_details=user_details, user_name=session['name'])


@bp.route('/about')
def about():
    return render_template('about.html', user_name=session['name'])


@bp.route('/edit_profile', methods=['post'])
def edit_profile():
    fname = request.form.get("fname").title()
    mname = request.form.get('mname').title()
    lname = request.form.get('lname').title()
    email = request.form.get('remail').lower()
    phone = request.form.get('rphone')
    dob = request.form.get('dob')
    sex = request.form.get('sex')
    query = """UPDATE `users` SET `fname` = '{}', `mname` = '{}', `lname` = '{}', `dob` = '{}',
     `email` = '{}', `phone` = '{}', `sex_id` = '{}' WHERE `users`.`user_id` = {};""".format(fname, mname, lname, dob,
                                                                                             email, phone, sex,
                                                                                             session['user_id'])
    __ = run_in_database(query, commit='yes')
    session['name'] = fname
    return redirect('/my_account')


@bp.route('/settings/<string:notice>')
def settings(notice):
    if notice == "none":
        notice = ''
    return render_template("settings.html", notice=notice, user_name=session['name'])


@bp.route('/get_subtype_of_type/<type_id>')
def get_sub_type(type_id):
    query = """SELECT 	`type_sub_type`.`sub_type_id`,`sub_type`.`subtype` FROM `type_sub_type`
    JOIN `sub_type` ON
    `type_sub_type`.`sub_type_id` = `sub_type`.`sub_type_id` WHERE `type_sub_type`.`type_id` = {}  ORDER BY `sub_type`.`subtype` ASC;""".format(
        type_id)
    result = run_in_database(quary=query, fetch='yes')
    return_obj = []
    for subtype in result:
        obj = {'id': subtype[0], 'subtype': subtype[1]}
        return_obj.append(obj)

    return jsonify(return_obj)


@bp.route('/add_table/<month>/<year>/<date>/<time>')
def add_table(month, year, date, time):
    date = date.replace("_", "-")
    time = time.replace("_", ":")
    if month == 'all' and year == 'all':
        month_filter = ""
    else:
        month_filter = """AND MONTH(date) = {}  AND YEAR(date) = {} """.format(datetime.strptime(month, '%B').month,
                                                                               year)
    query = """SELECT `expences`.`expence_name`,`expences`.`date`,`expences`.`time`,`credit_debit`.`type`,`type`.`type`,`sub_type`.`subtype`,`frequency`.`type`,`expences`.`amount`,`payment_medium`.`type`, `expences`.`expence_id` FROM 
    `expences` 

    JOIN `credit_debit` ON 
    `expences`.`credit_debit_id` = `credit_debit`.`credit_debit_id`

    JOIN `type` ON 
    `expences`.`type_id` = `type`.`type_id`

    JOIN `sub_type` ON
    `expences`.`sub_type_id` = `sub_type`.`sub_type_id`

    JOIN `frequency` ON
    `expences`.`frequency_id` = `frequency`.`frequency_id`

    JOIN `payment_medium` ON
    `expences`.`payment_medium_id` = `payment_medium`.`medium_id`

    WHERE `expences`.`user_id` = {}  {} AND ((`expences`.`date` = '{}' AND `expences`.`time` < '{}') OR  (`expences`.`date` < '{}'))

    ORDER BY `expences`.`date` DESC , `expences`.`time` DESC LIMIT 5 """.format(session['user_id'], month_filter, date,
                                                                                time, date)
    table_data = run_in_database(quary=query, fetch='yes')
    table_dict = []
    if table_data:
        if len(table_data) != 0:
            for i in table_data:
                row = []
                for j in i:
                    row.append(str(j))
                table_dict.append(row)
            return jsonify(table_dict)
        else:
            return jsonify(False)
    else:
        return jsonify(False)


@bp.route('/add_to_table/<table>/<value>')
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
