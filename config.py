import os

# DataBase configaration
# 1. Local
host = "localhost"
user = "root"
password = ""
database = "kharchakhata"


# # 2. AWS
# host = "database-2.csifl31dpmlc.us-east-2.rds.amazonaws.com"
# user = "admin"
# password = "9038383080"
# database = "kharchakhata"

# Email Configatation
email_user = "kharcha.khata.m2@gmail.com"
email_password = "Kharcha@123"


class Config:
    EXPLAIN_TEMPLATE_LOADING = True
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:9038383080@database-2.csifl31dpmlc.us-east-2.rds.amazonaws.com/kharchakhata'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@127.0.0.1/testing'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
