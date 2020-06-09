import os


class Config:
    # Email Configatation
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    EXPLAIN_TEMPLATE_LOADING = os.getenv("EXPLAIN_TEMPLATE_LOADING")
    SECRET_KEY = os.urandom(24)

    # Database Uri
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    # Google Login
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")

    # # facebook login
    # FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
    # FACEBOOK_CLIENT_SECRET = os.getenv()

    # aws s3 credentials
    ACCESS_ID = os.getenv("ACCESS_ID")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    S3_REGION = os.getenv("S3_REGION")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

    DEBUG = os.getenv("DEBUG")
