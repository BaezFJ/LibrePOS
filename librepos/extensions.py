from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mailman import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()