from flaskr.functions.authentication import *
from flaskr.functions.communication import *
from flaskr.functions.dash_figures import *
from flaskr.functions.database import *
from datetime import timedelta


def return_the_date_in_last_month(date):
    current_date = date.day
    if current_date > 29:
        return date.replace(day=1) - timedelta(days=1), (date.replace(day=1) - timedelta(days=1)).replace(day=1)
    else:
        return (date.replace(day=1) - timedelta(days=1)).replace(day=current_date), (
                date.replace(day=1) - timedelta(days=1)).replace(day=current_date).replace(day=1)



