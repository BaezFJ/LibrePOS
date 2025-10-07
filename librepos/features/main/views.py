from flask import render_template


def dashboard():
    context = {
        "head_title": "Dashboard",
    }
    return render_template("main/dashboard.html", **context)
