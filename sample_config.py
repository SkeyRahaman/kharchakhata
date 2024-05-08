class Config:
    # Basic Configurations
    SECRET_KEY = "your_secret_key_here"  # Replace with a secure, random secret key
    DEBUG = False  # Default to production setting

    # Email Configuration
    EMAIL_USERNAME = "your_email@example.com"
    EMAIL_PASSWORD = "your_email_password_here"

    # Database Configuration
    DB_TYPE = "mysql+mysqlconnector"  # Database type and connector (e.g., mysql+mysqlconnector, postgres)
    DB_USERNAME = "your_db_username_here"  # Database username
    DB_PASSWORD = "your_db_password_here"  # Database password
    DB_HOST = "127.0.0.1"  # Database host (localhost)
    DB_NAME = "your_db_name_here"  # Database name

    # Construct the full database URI from individual components
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary tracking
    SQLALCHEMY_ECHO = False  # Set to True for debugging SQL queries
    TIMEOUT = 180  # Database connection timeout in seconds

    # OAuth (Google and Facebook) Configuration
    GOOGLE_CLIENT_ID = "your_google_client_id_here"
    GOOGLE_CLIENT_SECRET = "your_google_client_secret_here"
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    FACEBOOK_CLIENT_ID = "your_facebook_client_id_here"
    FACEBOOK_CLIENT_SECRET = "your_facebook_client_secret_here"

    # AWS S3 Configuration
    ACCESS_ID = "your_aws_access_id_here"
    ACCESS_KEY = "your_aws_access_key_here"
    S3_REGION = "your_s3_region_here"  # Example: 'ap-south-1'
    S3_BUCKET_NAME = "your_s3_bucket_name_here"


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
