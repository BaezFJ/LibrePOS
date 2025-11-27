from flask_login import LoginManager
from flask_mailman import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from .database import BaseModel

db = SQLAlchemy(model_class=BaseModel)
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def init_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    setattr(login_manager, "login_view", "auth.login")
    login_manager.session_protection = "strong"

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from librepos.features.iam.repositories import IAMUserRepository

        return IAMUserRepository().get_by_id(user_id)
