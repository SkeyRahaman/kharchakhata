import os

class Config:
    # Email Configuration
    EMAIL_USERNAME = "dummy.email@example.com"
    EMAIL_PASSWORD = "DummyPassword123"

    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = 'dummysecretkey123456'
    # SECRET_KEY = os.urandom(24)

    # Database URI
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:dummy_password@dummy_database_url/kharchakhata2'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@127.0.0.1/dummy_database'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Login
    GOOGLE_CLIENT_ID = "dummy-google-client-id.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "dummy-google-client-secret"
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # AWS S3 credentials
    ACCESS_ID = "dummy-access-id"
    ACCESS_KEY = "dummy-access-key"
    S3_REGION = "ap-south-1"
    S3_BUCKET_NAME = "dummy-bucket-name"

    DEBUG = True
