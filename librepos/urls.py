def register_urls(app):
    @app.get("/")
    def index():
        return "LibrePOS Homepage."
