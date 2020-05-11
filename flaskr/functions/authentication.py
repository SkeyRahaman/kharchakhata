from flaskr.functions.database import *
from flask import session,flash


def login_with(email, password):
    quary = """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password)
    users = run_in_database(quary=quary, fetch='yes')

    if len(users) > 0:
        session['user_id'] = users[0][0]
        session['name'] = users[0][1]
        flash("Loged in as "+users[0][1], "success")
        return True
    else:
        return False


def login_with_for_admin(email, password):
    quary = """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' AND `admin` LIKE 1 ;""".format(
        email, password)
    users = run_in_database(quary=quary, fetch='yes')
    if users:
        if len(users) > 0:
            session['admin_user_id'] = users[0][0]
            session['admin_name'] = users[0][1]
        return True
    else:
        return False