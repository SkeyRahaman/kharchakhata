import os


class Config:
    # Email Configatation
    EMAIL_USERNAME = "kharcha.khata.m2@gmail.com"
    EMAIL_PASSWORD = "Kharcha@123"

    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = os.urandom(24)

    # Database Uri
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:9038383080@database-2.csifl31dpmlc.us-east-2.rds.amazonaws.com/kharchakhata2'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@127.0.0.1/testing2'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEOUT = 180

    # Google Login
    GOOGLE_CLIENT_ID = "1054655630563-eo9jbir0n130tup85vgros8srrof15jc.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "PG3GMDRYysLeGDSHO_EStP6v"
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # facebook login
    FACEBOOK_CLIENT_ID = "253088142772668"
    FACEBOOK_CLIENT_SECRET = "cd3edf3fce9a462edfd98b8e99241ffe"

    # aws s3 credentials
    ACCESS_ID = "AKIAITBOCNACLR5F6HTA"
    ACCESS_KEY = "ONLYLT90YpznIfNqPg6im42U412JOOWcyVuSBXGB"
    S3_REGION = "ap-south-1"
    S3_BUCKET_NAME = "kharchakhata-files"

    DEBUG = False