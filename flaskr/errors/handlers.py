from flask import Blueprint, render_template, redirect

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return redirect("/"), 404
