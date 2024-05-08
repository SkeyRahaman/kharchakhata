class Config:
    # Basic Configurations
    SECRET_KEY = "a0Xy9vRzX5JwQ8nBmS2fEoLg3DdJ7tKz"  # Secure, random secret key
    DEBUG = False  # Default to production setting

    # Email Configuration
    EMAIL_USERNAME = "kharcha.khata.m2@gmail.com"
    EMAIL_PASSWORD = "Kharcha@123"

    # Database Configuration
    DB_TYPE = "mysql+mysqlconnector"  # Database type and connector
    DB_USERNAME = "root"  # Database username
    DB_PASSWORD = ""  # Database password (empty string in this case)
    DB_HOST = "127.0.0.1"  # Database host (localhost)
    DB_NAME = "kharchakhatadb"  # Database name

    # Construct the full database URI from individual components
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary tracking
    SQLALCHEMY_ECHO = False
    TIMEOUT = 180  # Database connection timeout in seconds

    # OAuth (Google and Facebook) Configuration
    GOOGLE_CLIENT_ID = "1054655630563-eo9jbir0n130tup85vgros8srrof15jc.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "PG3GMDRYysLeGDSHO_EStP6v"
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    FACEBOOK_CLIENT_ID = "253088142772668"
    FACEBOOK_CLIENT_SECRET = "cd3edf3fce9a462edfd98b8e99241ffe"

    # AWS S3 Configuration
    ACCESS_ID = "AKIAITBOCNACLR5F6HTA"
    ACCESS_KEY = "ONLYLT90YpznIfNqPg6im42U412JOOWcyVuSBXGB"
    S3_REGION = "ap-south-1"
    S3_BUCKET_NAME = "kharchakhata-files"


class DevelopmentConfig(Config):
    DEBUG = True  # Enable debugging for development
    SQLALCHEMY_ECHO = True  # Log SQL queries for easier debugging


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True  # Log SQL queries during testing


class ProductionConfig(Config):
    DEBUG = False  # Disable debugging for production
    TESTING = False
    SQLALCHEMY_ECHO = False  # Disable query logging for production
