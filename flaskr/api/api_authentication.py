from flask import (Blueprint, redirect,
                   render_template, request,
                   jsonify, make_response)
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer

from flaskr.models import Users
from flaskr.functions import *
from flaskr import db, bcrypt, app
from datetime import datetime
from functools import wraps
import jwt

bp = Blueprint('api_auth', __name__,
               url_prefix='/api/auth')
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
email_link = URLSafeSerializer(app.config['SECRET_KEY'])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "token" in request.headers:
            token = request.headers['token']
        else:
            return jsonify({"message": "token missing"})
        try:
            data = jwt.decode(token.encode('utf-8'),
                              app.config["SECRET_KEY"])
            current_user = Users.query.filter_by(id=int(data['id'])).first()
            return f(current_user, *args, **kwargs)
        except Exception as e:
            print(str(e))
            return jsonify({"message": "invalid token"})

    return decorated


@bp.route('/login', methods=['POST'])
def login_and_get_token():
    data = request.get_json()
    if data and "email" in data and "password" in data:
        email = data['email']
        password = data['password']
        user = Users.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            print(app.config["SECRET_KEY"], type(app.config["SECRET_KEY"]))
            return jsonify({"token": jwt.encode({"id": user.id}, app.config["SECRET_KEY"]).decode('utf-8')})
        return make_response("invalid email and password.", 401, {'nothing': 'nothing'})
    return jsonify({'message': 'invalid body.!'})


@bp.route('/edit_user', methods=['POST'])
@token_required
def edit_user(current_user):
    data = request.get_json()
    if data:
        if "fname" in data and len(data["fname"]) > 0:
            current_user.fname = data['fname']

        if "mname" in data and len(data["mname"]) > 0:
            current_user.mname = data['mname']

        if "lname" in data and len(data["lname"]) > 0:
            current_user.lname = data['lname']

        if "dob" in data:
            try:
                current_user.dob = datetime.strptime(data['dob'], "%d/%m/%Y").date()
            except:
                return make_response("invalid date of birth format try 'DD/MM/YYYY!", 401, {'nothing': 'nothing'})

        if "email" in data:
            if data['email'] != current_user.email:
                if Users.query.filter_by(email=current_user.email).first():
                    return make_response("email address already present.!", 401, {'nothing': 'nothing'})
                current_user.email = data['email']
                current_user.email_conformation = 0

        if "phone" in data:
            current_user.phone = data['phone']

        if "password" in data:
            current_user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        if "sex_id" in data:
            current_user.sex_id = data['sex_id']

        if "picture" in data:
            current_user.picture = data['picture']

        db.session.commit()
    return jsonify({"message": "user edited"})


@bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if data:
        if "fname" in data and len(data["fname"]) > 0:
            fname = data['fname']
        else:
            return make_response("first name not found.!", 401, {'nothing': 'nothing'})

        if "mname" in data:
            mname = data['mname']
        else:
            mname = None

        if "lname" in data and len(data["lname"]) > 0:
            lname = data['lname']
        else:
            return make_response("last name not found.!", 401, {'nothing': 'nothing'})

        if "picture" in data:
            picture = data['picture']
        else:
            picture = None

        if "dob" in data:
            dob = datetime.strptime(data['dob'], "%d/%m/%Y").date()
        else:
            dob = None

        if "email" in data:
            email = data['email']
            if Users.query.filter_by(email=email).first():
                return make_response("email address already present.!", 401, {'nothing': 'nothing'})
        else:
            return make_response("email not found.!", 401, {'nothing': 'nothing'})

        if "email_conformation" in data:
            email_conformation = data['email_conformation']
        else:
            email_conformation = 0

        if "phone" in data:
            phone = data['phone']
        else:
            phone = None

        if ("external_auth" in data) and (data['external_auth'] == "1"):
            password = "External Website Verified."
        else:
            if "password" in data:
                password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            else:
                return make_response("password not found.!", 401, {'nothing': 'nothing'})

        if "sex_id" in data:
            sex_id = data['sex_id']
        else:
            sex_id = 4
        send_conformation_mail_before_login(email)
        new_user = Users(email=email, fname=fname,
                         mname=mname, lname=lname,
                         dob=dob, password=password,
                         phone=phone, sex=sex_id,
                         email_conformation=email_conformation, picture=picture)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Account created!"})
    return make_response("No data found!.", 401, {'nothing': 'nothing'})


@bp.route('/send_password_reset_email_for/<email>')
def send_password_reset_email_for(email):
    if "@" in str(email) and ".com" in str(email):
        user = Users.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt="this_is_the_email")
            reset_url = "https://" + str(request.host) + "/api/reset_password/" + str(token)
            send_mail(to=email, name=Users.query.filter_by(email=email).first().fname,
                      reset_url=reset_url)
            return jsonify({"message": "email send!."})
        return jsonify({"message": "email address not present"})
    else:
        return make_response("invalid email address.!")


@bp.route('/get_user')
@token_required
def get_user(current_user):
    try:
        dob = current_user.dob.strftime("%d/%m/%Y")
    except Exception as e:
        dob = None
    return jsonify({
        "fname": current_user.fname,
        "mname": current_user.mname,
        "lname": current_user.lname,
        "picture": current_user.picture,
        "email": current_user.email,
        "dob": str(dob),
        "email_conformation": current_user.email_conformation,
        "phone": current_user.phone,
        "sex_id": current_user.sex_id
    })


@bp.route('/remove_dp')
@token_required
def remove_dp(current_user):
    user = Users.query.filter_by(email=current_user.email).first()
    user.picture = None
    db.session.commit()
    return redirect("/my_account")


@bp.route('/send_conformation_mail_after_login')
@token_required
def send_conformation_mail_after_login(current_user):
    token = email_link.dumps(current_user.email, salt="this_is_the_email")
    conform_url = "https://" + str(request.host) + "/conform_email/" + str(token)
    try:
        send_welcome_email(email=current_user.email, fname=current_user.fname, conform_url=conform_url)
        return jsonify({"message": "email send.!"})
    except:
        return jsonify({"message": "email connection error"})


@bp.route('/send_conformation_mail_before_login/<email>')
def send_conformation_mail_before_login(email):
    current_user = Users.query.filter_by(email=email).first()
    token = email_link.dumps(email, salt="this_is_the_email")
    conform_url = "https://" + str(request.host) + "/conform_email/" + str(token)
    try:
        print(conform_url)
        send_welcome_email(email=current_user.email, fname=current_user.fname, conform_url=conform_url)
        return jsonify({"message": "email send.!"})
    except:
        return jsonify({"message": "email connection error"})
