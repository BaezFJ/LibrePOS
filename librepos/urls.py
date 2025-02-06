from flask import redirect, url_for

from librepos.blueprints import blueprints


def register_urls(app):
    @app.get("/")
    def index():
        return redirect(url_for("user.get_dashboard"))

    for bp in blueprints:
        app.register_blueprint(bp)
