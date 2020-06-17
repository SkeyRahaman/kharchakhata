from flask import Blueprint, render_template, request
from flaskr.models import Android
from flaskr.forms import App_edit, App_submit
from flask_login import login_required, current_user

bp = Blueprint('download', __name__,
               static_folder='static',
               template_folder="templates",
               url_prefix="/android")


@bp.route('/')
def android():
    apps = Android.query.filter_by(approved=1)
    print(apps)
    return render_template("android.html",
                           apps=apps)


@bp.route('/app_submit', methods=['GET', 'POST'])
def add_app():
    form = App_submit()
    if request.method == 'POST':
        print(form.errors)
    return render_template('add_app.html',
                           form=form)


@bp.route('/app_edit', methods=['POST'])
def edit_app():
    form = App_edit()
    if request.method == 'POST' and form.validate_on_submit():
        pass
    else:
        form.app_name.default = "hi"
    return render_template('edit_app.html',
                           form=form)
