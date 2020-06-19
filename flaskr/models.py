from flaskr import db, loginmanager
from flask_login import UserMixin
from datetime import datetime
from flask_login import current_user


@loginmanager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Sex(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(25), unique=True, nullable=False)
    user = db.relationship('Users', backref='sex', lazy=True)
    admin = db.relationship('Admin', backref='sex', lazy=True)

    def __repr__(self):
        return '<Sex %r>' % self.type


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
    comments = db.Column(db.String(100))

    def __repr__(self):
        return self.name

    def __init__(self, name, date_time,
                 type_subtype, frequency, payment,
                 debit, credit, user, comment):
        self.name = name
        self.date_time = date_time
        self.type_subtype_id = type_subtype
        self.frequency_id = frequency
        self.payment_id = payment
        self.debit = debit
        self.credit = credit
        self.user_id = user
        self.comments = comment


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(15), nullable=False)
    mname = db.Column(db.String(15))
    lname = db.Column(db.String(15))
    picture = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_conformation = db.Column(db.Integer, nullable=False, default=0)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(60), nullable=False)
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"), nullable=False)
    active = db.Column(db.Integer, default=1)
    expence_id = db.relationship('Expences', backref='user', lazy=True)
    android_id = db.relationship('Android', backref='android', lazy=True)

    def __repr__(self):
        return f"Users('{self.fname}','{self.email}','{self.password}')"

    def __init__(self,
                 fname, email, password,
                 mname=None, lname=None,
                 dob=None, phone=None,
                 sex=1, email_conformation=0,
                 picture=None):
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.picture = picture
        self.dob = dob
        self.email = email
        self.phone = phone
        self.password = password
        self.sex_id = sex
        self.email_conformation = email_conformation


class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    expence_id = db.relationship('Expences', backref='frequency', lazy=True)

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name


class Payment_medium(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    expence_id = db.relationship('Expences', backref='payment_medium', lazy=True)

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name


class Type_subtype(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey("type.id"), nullable=False)
    subtype_id = db.Column(db.Integer, db.ForeignKey("sub_type.id"), nullable=False)
    expence_id = db.relationship('Expences', backref='type_subtype', lazy=True)

    def __repr__(self):
        return self.id

    def __init__(self, type_id, subtype_id):
        self.type_id = type_id
        self.subtype_id = subtype_id


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    type_subtype_id = db.relationship('Type_subtype', backref='type', lazy=True)

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name


class Sub_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    type_subtype_id = db.relationship('Type_subtype', backref='subtype', lazy=True)

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(15), nullable=False)
    mname = db.Column(db.String(15))
    lname = db.Column(db.String(15))
    picture = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(60), unique=True, nullable=False)
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


class Android(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_name = db.Column(db.String(40), nullable=False)
    app_logo_url = db.Column(db.String(100))
    dev_name = db.Column(db.String(60), nullable=False)
    intro1 = db.Column(db.String(80), nullable=False)
    intro2 = db.Column(db.String(80), nullable=False)
    app_url = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dev_profile_url = db.Column(db.String(100), default="#")
    date_time = db.Column(db.DateTime, nullable=False)
    approved = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Android name %r>' % self.app_name

    def __init__(self, app_name, app_logo_url,
                 dev_name, intro1, intro2,
                 app_url, user_id, dev_profile_url="#",
                 ):
        self.app_name = app_name
        self.app_logo_url = app_logo_url
        self.dev_name = dev_name
        self.intro1 = intro1
        self.intro2 = intro2
        self.app_url = app_url
        self.user_id = user_id
        self.dev_profile_url = dev_profile_url
        self.date_time = datetime.now()
        self.approved = 0
