from flask import Blueprint, render_template, redirect
import itsdangerous.exc
import sqlalchemy.exc

errors = Blueprint('errors', __name__,
                   template_folder='templates', )


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("error_404.html"), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("error_500.html"), 500


@errors.app_errorhandler(itsdangerous.exc.BadSignature)
def error_500(error):
    return render_template("error_mail_url.html"), 500


@errors.app_errorhandler(sqlalchemy.exc.OperationalError)
@errors.app_errorhandler(sqlalchemy.exc.StatementError)
@errors.app_errorhandler(sqlalchemy.exc.InterfaceError)
def error_db(error):
    return render_template("error_db_connection.html"), 500
