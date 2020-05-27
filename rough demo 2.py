from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@127.0.0.1/testing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Expences(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    type_subtype_id = db.Column(db.Integer, db.ForeignKey("type_subtype.id"), nullable=False)
    frequency_id = db.Column(db.Integer, db.ForeignKey("frequency.id"), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment_medium.id"), nullable=False)
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return self.name


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(15), nullable=False)
    mname = db.Column(db.String(15))
    lname = db.Column(db.String(15))
    dob = db.Column(db.Date)
    email = db.Column(db.String(30), unique=True, nullable=False)
    email_conformation = db.Column(db.Integer, nullable=False, default=0)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(60), nullable=False)
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"), nullable=False)
    active = db.Column(db.Integer, default=1)
    expence_id = db.relationship('Expences', backref='user', lazy=True)

    def __repr__(self):
        return f"Users('{self.fname}','{self.email}','{self.password}')"

    def __init__(self,
                 fname, email, password,
                 mname=None, lname=None,
                 dob=None, phone=None,
                 id=None, sex=4):
        self.id = id
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.dob = dob
        self.email = email
        self.phone = phone
        self.password = password
        self.sex_id = sex


class Sex(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), unique=True, nullable=False)
    user = db.relationship('Users', backref='sex', lazy=True)
    admin = db.relationship('Admin', backref='sex', lazy=True)

    def __repr__(self):
        return '<Sex %r>' % self.type


class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    expence_id = db.relationship('Expences', backref='frequency', lazy=True)

    def __repr__(self):
        return self.name


class Payment_medium(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    expence_id = db.relationship('Expences', backref='payment_medium', lazy=True)

    def __repr__(self):
        return self.name


class Type_subtype(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey("type.id"), nullable=False)
    subtype_id = db.Column(db.Integer, db.ForeignKey("sub_type.id"), nullable=False)
    expence_id = db.relationship('Expences', backref='type_subtype', lazy=True)

    def __repr__(self):
        return self.id


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    type_subtype_id = db.relationship('Type_subtype', backref='type', lazy=True)

    def __repr__(self):
        return self.name


class Sub_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    type_subtype_id = db.relationship('Type_subtype', backref='subtype', lazy=True)

    def __repr__(self):
        return self.name


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(15), nullable=False)
    mname = db.Column(db.String(15))
    lname = db.Column(db.String(15))
    dob = db.Column(db.Date)
    email = db.Column(db.String(30), unique=True, nullable=False)
    email_conformation = db.Column(db.Integer, nullable=False, default=0)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(60), nullable=False)
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"), nullable=False)
    active = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"Users('{self.fname}','{self.email}','{self.password}')"

    def __init__(self,
                 fname, email, password,
                 mname=None, lname=None,
                 dob=None, phone=None,
                 id=None, sex=4):
        self.id = id
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.dob = dob
        self.email = email
        self.phone = phone
        self.password = password
        self.sex = sex


@app.route('/')
def index():
    res = Type_subtype.query.filter_by(type_id=1)
    for r in res:
        print(r.subtype)
    return ""


@app.route('/get_subtype_of_type/<type_id>')
def get_sub_type(type_id):
    subtypes = Type_subtype.query.filter_by(type_id=type_id)
    print(subtypes)
    subtype_obj = []
    for i in subtypes:
        obj = {
            'id': int(i.subtype_id),
            'subtype': str(i.subtype)
        }
        subtype_obj.append(obj)
    return jsonify(subtype_obj)


if __name__ == "__main__":
    app.run(debug=True)
