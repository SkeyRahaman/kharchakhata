from flask import Blueprint, redirect, render_template, request, jsonify

bp = Blueprint('api', __name__,
               url_prefix='/api')


@bp.route("/")
def index():
    return jsonify({"name": "shakib mondal"})
