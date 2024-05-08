from flask import Blueprint, render_template, request, flash, redirect, abort, url_for
from flaskr.models import Android, Users
from flaskr.forms import App_edit, App_submit
from flask_login import login_required, current_user
from flaskr import db, app
import boto3
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('android_bp', __name__,
               static_folder='static',
               template_folder="templates",
               url_prefix="/android")


@bp.route('/')
def android():
    apps = db.session.query(Android) \
        .filter(Android.date_time.in_(db.session.query(func.max(Android.date_time)) \
                                      .filter(Android.approved == 1) \
                                      .group_by(Android.user_id).subquery()))
    if current_user.is_authenticated:
        my_apps = Android.query.filter(Android.user_id == current_user.id).all()
    else:
        my_apps = None
    return render_template("android.html",
                           apps=apps,
                           my_apps=my_apps)


@bp.route('/app_submit', methods=['GET', 'POST'])
@login_required
def add_app():
    form = App_submit()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('app_name')
        image = request.files["app_logo"]
        app_ = request.files["app"]
        app_icon_name = "android_app_icon_" + datetime.now().strftime("_%H_%M_%S_%d_%m_%Y_") + str(
            current_user.id) + "." + \
                        image.filename.split(".")[-1]
        app_name = "android_app_icon_" + datetime.now().strftime("_%H_%M_%S_%d_%m_%Y_") + str(current_user.id) + "." + \
                   app_.filename.split(".")[-1]
        s3_1 = boto3.resource('s3',
                              aws_access_key_id=app.config["ACCESS_ID"],
                              aws_secret_access_key=app.config["ACCESS_KEY"]
                              )
        s3_1.Bucket("kharchakhata-files") \
            .put_object(Key=app_icon_name, Body=image, ACL='public-read')
        s3_2 = boto3.resource('s3',
                              aws_access_key_id=app.config["ACCESS_ID"],
                              aws_secret_access_key=app.config["ACCESS_KEY"]
                              )
        s3_2.Bucket("kharchakhata-files") \
            .put_object(Key=app_name, Body=app_, ACL='public-read')
        app_logo_url = "https://s3-{}.amazonaws.com/{}/{}".format(
            app.config["S3_REGION"],
            app.config['S3_BUCKET_NAME'],
            app_icon_name
        )
        app_url = "https://s3-{}.amazonaws.com/{}/{}".format(
            app.config["S3_REGION"],
            app.config['S3_BUCKET_NAME'],
            app_name
        )
        dev_name = request.form.get('dev_name')
        intro1 = request.form.get('intro1')
        intro2 = request.form.get('intro2')
        dev_profile_url = request.form.get('dev_profile_url')
        application = Android(app_name=name,
                              app_logo_url=app_logo_url,
                              app_url=app_url,
                              dev_name=dev_name,
                              intro1=intro1,
                              intro2=intro2,
                              dev_profile_url=dev_profile_url,
                              user_id=current_user.id
                              )
        db.session.add(application)
        db.session.commit()
        flash("Application Upload successful, Your application will come online after we verify your application.",
              "success")
        return redirect('/android')
    form.dev_name.default = str(current_user.fname) + " " + str(current_user.mname) + " " + str(current_user.lname)
    form.process()
    return render_template('add_app.html',
                           form=form)


@bp.route('/app_edit/<app_id>', methods=['GET', 'POST'])
@login_required
def edit_app(app_id):
    form = App_edit()
    if request.method == 'POST' and form.validate_on_submit():
        app = db.session.query(Android) \
            .filter(Android.id == app_id) \
            .filter(Android.user_id == current_user.id) \
            .first()
        app.name = request.form.get('app_name')
        app.dev_name = request.form.get('dev_name')
        app.intro1 = request.form.get('intro1')
        app.intro2 = request.form.get('intro2')
        app.dev_profile_url = request.form.get('dev_profile_url')
        db.session.commit()
        flash("Change has been Submitted!", "success")
        return redirect('/android')
    else:
        app = db.session.query(Android) \
            .filter(Android.id == app_id) \
            .filter(Android.user_id == current_user.id) \
            .first()
        form.app_name.default = app.app_name
        form.dev_name.default = app.dev_name
        form.intro1.default = app.intro1
        form.intro2.default = app.intro2
        form.dev_profile_url.default = app.dev_profile_url
        form.process()
    return render_template('edit_app.html',
                           form=form,
                           app_id=app_id)


@bp.route('/delete/<id>')
@login_required
def delete_application(id):
    app = db.session.query(Android).filter(Android.id == id).first()
    if app and app.user_id == current_user.id:
        db.session.delete(app)
        db.session.commit()
        flash("Application Removed.!!", "danger")
    return redirect("/android")
