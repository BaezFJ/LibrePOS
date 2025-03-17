from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user

from librepos.models import UserProfile
from librepos.models.user import User, UserStatus
from librepos.utils.helpers import sanitize_form_data
from librepos.utils.messages import Messages, display_message
from .forms import LoginForm, NewUserForm, UserProfileForm


class UserController:

    def __init__(self):
        self.login_url = url_for("user.login")
        self.dashboard_url = url_for("user.dashboard")

        self.user_model = User

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
                    target_profile_url = url_for("user.profile", user_id=user.id)
                    display_message(Messages.AUTH_LOGIN)
                    return redirect(target_profile_url)

                display_message(Messages.AUTH_LOGIN)
                return redirect(self.dashboard_url)

            display_message(Messages.AUTH_FAILED)
            return redirect(self.login_url)
        return render_template("user/login.html", **context)

    def handle_logout(self):
        logout_user()
        display_message(Messages.AUTH_LOGOUT)
        return redirect(self.login_url)

    def list_users(self):
        _users = User.get_all()
        form = NewUserForm()
        context = {
            "title": "Users",
            "users": _users,
            "form": form,
            "back_url": self.dashboard_url
        }
        return render_template("user/list_users.html", **context)

    def profile(self):
        _user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
        form = UserProfileForm(obj=_user_profile)
        context = {
            "title": "Profile",
            "form": form,
            "back_url": self.dashboard_url,
        }
        if form.validate_on_submit():
            sanitized_data = sanitize_form_data(form)
            user_id = current_user.id
            if _user_profile is None:
                UserProfile.create(user_id=user_id, **sanitized_data)
            else:
                UserProfile.update(user_id, **sanitized_data)
            display_message(Messages.USER_PROFILE_UPDATED)
            return redirect(self.dashboard_url)
        return render_template("user/profile.html", **context)

    def edit_user(self, user_id: str):
        _user = self.user_model.query.filter_by(id=user_id).first_or_404()
        context = {
            "title": "Edit User",
            "user": _user,
            "back_url": url_for("user.list_users"),
        }
        return render_template("user/edit_user.html", **context)

    @staticmethod
    def dashboard():
        context = {
            "title": "Dashboard"
        }
        return render_template("user/dashboard.html", **context)
