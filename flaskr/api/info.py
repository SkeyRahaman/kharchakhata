from flask import Blueprint, render_template

bp = Blueprint('api_info', __name__,
               url_prefix='/api/info',
               template_folder='templates')


@bp.route('/')
def api_info_home():
    return render_template("api.html")
