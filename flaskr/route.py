from flask import redirect, render_template, request, url_for, jsonify
from flaskr import app, bcrypt, db
from flaskr.functions import *
from flaskr.models import Expences, Type_subtype, Type, Frequency, Payment_medium
from flaskr.forms import Reset_password, Expence_form
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import func
import os


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
    else:
        form.type.choices = [(type.id, type.name) for type in Type.query.all()]
        form.frequency.choices = [(fre.id, fre.name) for fre in Frequency.query.all()]
        form.payment_method.choices = [(payment_method.id, payment_method.name) for payment_method in
                                       Payment_medium.query.all()]

    return render_template("add_expence.html", form=form, title="Add Transaction")


@app.route("/delete_expence/<id>")
@login_required
def delete_expence(id):
    b = Expences.query.filter_by(id=id).first()
    if b.user_id == current_user.id:
        Expences.query.filter_by(id=id).delete()
        db.session.commit()
        flash("Transaction Deleted :( ", "danger")
        return redirect("/")
    else:
        flash("This is not your data to delete!", "danger")
        return redirect("/")


@app.route("/edit_expence/<id>", methods=["GET", "POST"])
@login_required
def edit_expence(id):
    id = int(id)
    form = Expence_form()
    b = Expences.query.filter_by(id=id).first()
    if b.user_id == current_user.id:
        if request.method == 'POST' and form.validate_on_submit():
            expence = Expences.query.filter_by(id=id).first()
            expence.name = request.form.get("name").title()
            date = request.form.get("date")
            amount = request.form.get("amount")
            time = request.form.get("time")
            expence.date_time = datetime.strptime((date + " " + time), '%Y-%m-%d %H:%M')
            expence.user_id = current_user.id
            transaction_type = request.form.get("transaction_type")
            expence.type_subtype_id = request.form.get("subtype")
            expence.frequency_id = request.form.get("frequency")
            expence.payment_method = request.form.get("payment_method")
            expence.comments = request.form.get("comment")
            if transaction_type == "1":
                expence.debit = amount
                expence.credit = 0
            else:
                expence.debit = 0
                expence.credit = amount
            db.session.commit()
            flash("Transaction saved.", "success")
            return redirect("/")
        else:
            form.type.choices = [(type.id, type.name) for type in Type.query.all()]
            form.type.default = Type_subtype.query.filter_by(id=b.type_subtype_id).first().type_id
            form.frequency.choices = [(fre.id, fre.name) for fre in Frequency.query.all()]
            form.frequency.default = b.frequency_id
            form.payment_method.choices = [(payment_method.id, payment_method.name) for payment_method in
                                           Payment_medium.query.all()]
            form.payment_method.default = b.payment_id
            subtypes = Type_subtype.query \
                .filter_by(type_id=Type_subtype.query.filter_by(id=b.type_subtype_id).first().type_id)
            form.subtype.choices = [[i.id, i.subtype] for i in subtypes]
            form.subtype.default = b.type_subtype_id
            if b.credit == 0:
                form.transaction_type.default = 1
            else:
                form.transaction_type.default = 2
            form.process()

            form.name.data = b.name
            form.date.data = b.date_time.date()
            form.time.data = b.date_time.time()
            if b.credit == 0:
                form.amount.data = b.debit
            else:
                form.amount.data = b.credit
            form.comment.data = b.comments

            return render_template("edit_expense.html", form=form, title="Edit Transaction", id=id)
    else:
        flash("This is not your data to edit!", "danger")
        return redirect("/")


@app.route('/add_table/<month>/<year>/<id>')
@login_required
def add_table(month, year, id):
    last_expence_time = Expences.query.filter_by(id=id).first().date_time
    if month == 'all':
        table_data_touple = db.session.query(Expences) \
            .order_by(Expences.date_time.desc()) \
            .filter(Expences.user_id == current_user.id) \
            .filter(Expences.date_time <= last_expence_time) \
            .filter(Expences.id != id) \
            .limit(10)
    else:
        table_data_touple = db.session.query(Expences) \
            .order_by(Expences.date_time.desc()) \
            .filter(Expences.user_id == current_user.id) \
            .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
            .filter(func.year(Expences.date_time) == int(year)) \
            .filter(Expences.date_time <= last_expence_time) \
            .filter(Expences.id != id) \
            .limit(2)
    table_data = []
    for row in table_data_touple:
        table_data.append({
            'id': str(row.id),
            'name': str(row.name),
            'date': str(row.date_time.strftime('%d %B, %Y')),
            'time': str(row.date_time.strftime('%I:%M %p')),
            'type': str(row.type_subtype.type),
            'subtype': str(row.type_subtype.subtype),
            'frequency': str(row.frequency),
            'debit': int(row.debit),
            'credit': int(row.credit),
            'payment_method': str(row.payment_medium),
            'comment': str(row.comments)
        })
    if table_data:
        return jsonify(table_data)
    else:
        return jsonify(False)


@app.route('/dashboard/<string:month>/<string:year>')
@login_required
def dashboard(month, year):
    if month == 'all':
        credit_debit_saving = db.session.query(func.sum(Expences.credit).label("credit"),
                                               func.sum(Expences.debit).label("debit"),
                                               (func.sum(Expences.credit) - func.sum(Expences.debit)).label("savings")) \
            .filter(Expences.user_id == current_user.id) \
            .first()
        table_data_touple = db.session.query(Expences) \
            .order_by(Expences.date_time.desc()) \
            .filter(Expences.user_id == current_user.id) \
            .limit(20)
    else:
        credit_debit_saving = db.session.query(func.sum(Expences.credit).label("credit"),
                                               func.sum(Expences.debit).label("debit"),
                                               (func.sum(Expences.credit) - func.sum(Expences.debit)).label("savings")) \
            .filter(Expences.user_id == current_user.id) \
            .filter((func.month(Expences.date_time) == datetime.strptime(month, '%B').month)) \
            .filter(func.year(Expences.date_time) == int(year)) \
            .first()
        table_data_touple = db.session.query(Expences) \
            .order_by(Expences.date_time.desc()) \
            .filter(Expences.user_id == current_user.id) \
            .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
            .filter(func.year(Expences.date_time) == int(year)) \
            .limit(20)
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
    table_data = []
    for row in table_data_touple:
        table_data.append({
            'id': row.id,
            'name': row.name,
            'date': row.date_time.strftime('%d %B, %Y'),
            'time': row.date_time.strftime('%I:%M %p'),
            'type': row.type_subtype.type,
            'subtype': row.type_subtype.subtype,
            'frequency': row.frequency,
            'debit': row.debit,
            'credit': row.credit,
            'payment_method': row.payment_medium,
            'comment': row.comments
        })
    month_name = db.session.query(func.month(Expences.date_time),
                                  func.year(Expences.date_time)).filter(Expences.user_id == current_user.id).distinct()
    _ = sorted([[i[0], i[1], calendar.month_name[i[0]]] for i in month_name], key=lambda x: (x[1], x[0]), reverse=True)
    month_name = [[i[2], i[1]] for i in _]

    return render_template('dashboard.html',
                           title="Dashboard",
                           months=month_name,
                           card=card,
                           table=table_data)


@app.route('/about')
def about():
    return render_template('about.html',
                           title="About")


@app.route('/settings', methods=["get", "post"])
@login_required
def settings():
    form_password = Reset_password()
    if form_password.validate_on_submit():
        cpassword = request.form.get('password')
        if cpassword:
            if bcrypt.check_password_hash(current_user.password, cpassword):
                current_user.password = bcrypt.generate_password_hash(request.form.get('cnpassword')).decode('utf-8')
                db.session.commit()
                flash("Password Updated Successful!.", "success")
            else:
                flash("Current Password Does Not Match!", "danger")
        elif current_user.password == "External Website Verified.":
            current_user.password = bcrypt.generate_password_hash(request.form.get('cnpassword')).decode('utf-8')
            db.session.commit()
            flash("Password Updated Successful!.", "success")
        else:
            flash("Please enter your current password.", "info")
    return render_template("settings.html",
                           form_password=form_password,
                           title="Settings")


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
