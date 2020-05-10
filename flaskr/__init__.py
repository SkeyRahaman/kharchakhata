from flask import Flask
import os
from itsdangerous import URLSafeTimedSerializer


def create_app():
    app = Flask(__name__)
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True
    app.secret_key = os.urandom(24)
    app.config['SECRET_KEY'] = os.urandom(24)

    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    from . import auth, route
    app.register_blueprint(auth.bp)
    app.register_blueprint(route.bp)

    from flaskr.dashboard_dash.dashboard import create_dashboard
    app = create_dashboard(app)

    return app
