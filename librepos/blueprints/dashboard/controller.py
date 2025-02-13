from flask import render_template


class DashboardController:

    @staticmethod
    def show_dashboard():
        context = {
            "title": "Dashboard",
        }
        return render_template("dashboard/dashboard.html", **context)

    @staticmethod
    def show_overview():
        context = {
            "title": "Overview"
        }
        return render_template("dashboard/overview.html", **context)
