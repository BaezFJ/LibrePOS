from librepos.routes.dashboard import dashboard_bp
from librepos.routes.auth import auth_bp

def register_urls(app):

    @app.get("/")
    def index():
        return "LibrePOS Homepage."

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
