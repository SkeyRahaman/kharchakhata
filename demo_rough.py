from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@127.0.0.1/kharchakhatadb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:9038383080@database-1.csifl31dpmlc.us-east-2.rds.amazonaws.com/kharchakhata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    fname = db.Column('fname', db.Unicode)
    mname = db.Column('mname', db.Unicode)
    lname = db.Column('lname', db.Unicode)
    dob = db.Column('dob', db.Date)
    email = db.Column('email', db.Unicode)
    phone = db.Column('phone', db.Unicode)
    password = db.Column('password', db.Unicode)
    sex = db.Column('sex', db.Integer) 
    active = db.Column('active', db.Integer)




class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column('user_id', db.Integer, primary_key=True)
    fname = db.Column('fname', db.Unicode)
    mname = db.Column('mname', db.Unicode)
    lname = db.Column('lname', db.Unicode)
    dob = db.Column('dob', db.Date)
    email = db.Column('email', db.Unicode)
    phone = db.Column('phone', db.Unicode)
    password = db.Column('password', db.Unicode)
    sex = db.Column('sex', db.Integer)
    active = db.Column('active', db.Integer)



class Expences(db.Model):
    __tablename__ = "expences"
    id = db.Column('expence_id', db.Integer, primary_key=True)
    name = db.Column('expence_name', db.Unicode)
    date = db.Column('date', db.Date)
    time = db.Column('time', db.Time)
    credit = db.Column('credit', db.Float)
    debit = db.Column('debit', db.Float)
    user = db.Column('user_id', db.Integer)
    frequency = db.Column('frequency_id', db.Integer)
    payment = db.Column('payment_medium_id', db.Integer)
    type = db.Column('type_subtype_id', db.Integer)




class Frequency(db.Model):
    __tablename__ = "frequency"
    id = db.Column('frequency_id', db.Integer, primary_key=True)
    type = db.Column('frequency', db.Unicode)




class Payment_medium(db.Model):
    __tablename__ = "payment_medium"
    id = db.Column('medium_id', db.Integer, primary_key=True)
    type = db.Column('type', db.Unicode)



class Sex(db.Model):
    __tablename__ = "sex"
    id = db.Column('sex_id', db.Integer, primary_key=True)
    type = db.Column('type', db.Unicode)



class Sub_type(db.Model):
    __tablename__ = "sub_type"
    id = db.Column('sub_type_id', db.Integer, primary_key=True)
    type = db.Column('subtype', db.Unicode)


class Type(db.Model):
    __tablename__ = "type"
    id = db.Column('type_id', db.Integer, primary_key=True)
    type = db.Column('type', db.Unicode)


class Type_subtype(db.Model):
    __tablename__ = "type_subtype"
    id = db.Column('type_subtype_id', db.Integer, primary_key=True)
    type = db.Column('type_id', db.Integer)
    sub_type = db.Column('sub_type_id', db.Integer)
print(Type_subtype.query.all()[0].type)

print(Users.query.all()[0].fname)
