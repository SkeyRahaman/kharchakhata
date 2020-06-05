from flaskr.functions.database import *
from flask import session, flash, request
from flaskr import app
import requests


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


def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
