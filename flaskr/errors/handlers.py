from flask import Blueprint, render_template, redirect

errors = Blueprint('errors', __name__,
                   template_folder='templates',)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("error_404.html"), 404
