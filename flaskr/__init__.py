from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

loginmanager = LoginManager(app)
loginmanager.login_view = 'home'
loginmanager.login_message_category = 'info'

with app.app_context():
    from flaskr.authentication import auth

    app.register_blueprint(auth.bp)

    from flaskr.route import *

    from flaskr.dashboard_dash.dashboard import create_dashboard

    app = create_dashboard(app)
