import os

from dotenv import load_dotenv

load_dotenv()


def strtobool(val):
    val = val.lower()
    if val in ("yes", "true", "t", "1"):
        return True
    elif val in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


# Application Settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TIMEZONE = os.getenv("TIMEZONE", "US/Central")
LOCAL_NETWORK = os.getenv("LOCAL_NETWORK", "192.168.0.0/16")
COMPANY_NAME = os.getenv("COMPANY_NAME", "LibrePOS")

# Flask Settings
DEBUG = os.getenv("DEBUG", False)
TESTING = os.getenv("TESTING", False)

if DEBUG or TESTING:
    SECRET_KEY = "development-and-testing-key-not-for-production"
else:
    SECRET_KEY = os.getenv("SECRET_KEY")

# Flask-SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mailman
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", False)
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", False)
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND", False)
