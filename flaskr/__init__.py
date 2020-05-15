from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy()
db.init_app(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'home'
loginmanager.login_message_category = 'info'


with app.app_context():
    from . import auth
    app.register_blueprint(auth.bp)

    from flaskr.route import *

    from flaskr.dashboard_dash.dashboard import create_dashboard

    app = create_dashboard(app)
