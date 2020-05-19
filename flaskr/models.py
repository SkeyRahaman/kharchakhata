from flaskr import db, loginmanager
from flask_login import UserMixin


@loginmanager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Sex(db.Model, UserMixin):
    __tablename__ = "sex"
    id = db.Column("id", db.Integer, primary_key=True, unique=True, autoincrement=True)
    type = db.Column("type", db.String(10), unique=True)


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True, unique=True)
    fname = db.Column('fname', db.Unicode, nullable=False)
    mname = db.Column('mname', db.Unicode)
    lname = db.Column('lname', db.Unicode)
    dob = db.Column('dob', db.Date)
    email = db.Column('email', db.Unicode, unique=True, nullable=False)
    phone = db.Column('phone', db.Unicode)
    password = db.Column('password', db.Unicode, nullable=False)
    sex = db.Column('sex_id', db.Integer)
    active = db.Column('active', db.Integer)

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
        self.active = 1

