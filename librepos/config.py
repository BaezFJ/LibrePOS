import os

from dotenv import load_dotenv

load_dotenv()

# Application Settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TIMEZONE = os.getenv("TIMEZONE", "US/Central")
LOCAL_NETWORK = os.getenv("LOCAL_NETWORK", "192.168.0.0/16")

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
