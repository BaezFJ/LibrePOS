from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user

from librepos.models.user import User, UserStatus
from librepos.utils.messages import Messages, display_message
from .forms import LoginForm


class UserController:

    def __init__(self):
        self.login_url = url_for("user.login")
        self.dashboard_url = url_for("dashboard.get_dashboard")

    def handle_login(self):

        if current_user.is_authenticated:
            display_message(Messages.AUTH_LOGGED_IN)
            return redirect(self.dashboard_url)

        form = LoginForm()
        context = {"title": "Login", "form": form}

        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter_by(username=username, status=UserStatus.ACTIVE).first()
            locked_user = User.query.filter_by(username=username, status=UserStatus.LOCKED).first()

            if locked_user:
                display_message(Messages.AUTH_LOCKED)
                return redirect(self.login_url)

            if user and not user.check_password(form.password.data):
                display_message(Messages.AUTH_FAILED)
                user.activity.update_failed_login_attempts()
                return redirect(self.login_url)

            if user and user.check_password(form.password.data):
                if not user.is_active:
                    display_message(Messages.AUTH_LOCKED)
                    return redirect(self.login_url)

                login_user(user, remember=form.remember_me.data)
                ip_address = request.remote_addr
                device_info = request.user_agent.string
                user.activity.update_activity(ip_address=ip_address, device_info=device_info)

                if user.activity.login_count == 1:
                    target_profile_url = url_for("user.get_user_profile", user_id=user.id)
                    display_message(Messages.AUTH_LOGIN)
                    return redirect(target_profile_url)

                display_message(Messages.AUTH_LOGIN)
                return redirect(self.dashboard_url)

            display_message(Messages.AUTH_FAILED)
            return redirect(self.login_url)
        return render_template("user/login.html", **context)
