from flask import redirect, render_template, request, url_for, jsonify
from flaskr import app, bcrypt, db
from flaskr.functions import *
from flaskr.models import Expences, Type_subtype, Type, Frequency, Payment_medium
from flaskr.forms import Reset_password, Expence_form
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import func


@app.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    else:
        month = datetime.now().strftime("%B")
        year = datetime.now().year
        return redirect("/dashboard/{}/{}".format(month, year))


@app.route("/add_expence", methods=["GET", "POST"])
@login_required
def add_expence():
    form = Expence_form()
    form.type.choices = [(type.id, type.name) for type in Type.query.all()]
    form.frequency.choices = [(fre.id, fre.name) for fre in Frequency.query.all()]
    form.payment_method.choices = [(payment_method.id, payment_method.name) for payment_method in
                                   Payment_medium.query.all()]
    if form.validate_on_submit():
        expence_name = request.form.get("name").title()
        date = request.form.get("date")
        amount = request.form.get("amount")
        time = request.form.get("time")
        date_time = datetime.strptime((date + " " + time), '%Y-%m-%d %H:%M')
        user_id = current_user.id
        transaction_type = request.form.get("transaction_type")
        type_subtype = request.form.get("subtype")
        frequency = request.form.get("frequency")
        payment_method = request.form.get("payment_method")
        comment = request.form.get("comment")
        if transaction_type == "1":
            debit = amount
            credit = 0
        else:
            debit = 0
            credit = amount
        new_transaction = Expences(name=expence_name, date_time=date_time,
                                   type_subtype=type_subtype, frequency=frequency,
                                   payment=payment_method, credit=credit,
                                   debit=debit, user=user_id,
                                   comment=comment)
        db.session.add(new_transaction)
        db.session.commit()
        flash("New Transaction Added!", "success")
        return redirect("/")

    return render_template("add_expence.html", form=form)


@app.route('/dashboard/<string:month>/<string:year>')
@login_required
def dashboard(month, year):
    if month == 'all':
        credit_debit_saving = db.session.query(func.sum(Expences.credit).label("credit"),
                                               func.sum(Expences.debit).label("debit"),
                                               (func.sum(Expences.credit) - func.sum(Expences.debit)).label("savings")) \
            .filter(Expences.user_id == current_user.id).first()
    else:
        credit_debit_saving = db.session.query(func.sum(Expences.credit).label("credit"),
                                               func.sum(Expences.debit).label("debit"),
                                               (func.sum(Expences.credit) - func.sum(Expences.debit)).label("savings")) \
            .filter(Expences.user_id == current_user.id).filter(
            (func.month(Expences.date_time) == datetime.strptime(month, '%B').month)).filter(
            func.year(Expences.date_time) == int(year)).first()
    last_month_profit = db.session.query((func.sum(Expences.credit) - func.sum(Expences.debit)).label("savings")) \
        .filter(Expences.user_id == current_user.id).filter(
        func.month(Expences.date_time) == (datetime.now().month - 1)) \
        .first()
    card = {
        "credit": credit_debit_saving.credit,
        "debit": credit_debit_saving.debit,
        "saving": credit_debit_saving.savings,
        "last_month_saving": last_month_profit.savings
    }
    month_name = db.session.query(func.month(Expences.date_time),
                                  func.year(Expences.date_time)).distinct()
    _ = sorted([[i[0], i[1], calendar.month_name[i[0]]] for i in month_name], key=lambda x: (x[1], x[0]), reverse=True)
    month_name = [[i[2], i[1]] for i in _]
    if month == 'all':
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

        WHERE `expences`.`user_id` = {} {}

        ORDER BY `expences`.`date` DESC , `expences`.`time` DESC LIMIT 10 """.format(current_user.id,
                                                                                     month_filter)
    table_data = run_in_database(query, fetch='yes')

    return render_template('dashboard.html',
                           card=card,
                           table=table_data,
                           months=month_name)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/settings', methods=["get", "post"])
@login_required
def settings():
    form_password = Reset_password()
    if form_password.validate_on_submit():
        cpassword = request.form.get('password')
        if bcrypt.check_password_hash(current_user.password, cpassword):
            current_user.password = bcrypt.generate_password_hash(request.form.get('cnpassword')).decode('utf-8')
            db.session.commit()
            flash("Password Updated Successful!.", "success")
        else:
            flash("Current Password Does Not Match!", "danger")
    return render_template("settings.html", form_password=form_password)


@app.route('/get_subtype_of_type/<type_id>')
@login_required
def get_sub_type(type_id):
    subtypes = Type_subtype.query.filter_by(type_id=type_id)
    subtype_obj = []
    for i in subtypes:
        obj = {
            'id': int(i.id),
            'subtype': str(i.subtype)
        }
        subtype_obj.append(obj)
    return jsonify(subtype_obj)


@app.route('/add_table/<month>/<year>/<date>/<time>')
@login_required
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

    ORDER BY `expences`.`date` DESC , `expences`.`time` DESC LIMIT 5 """.format(current_user.id, month_filter, date,
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
