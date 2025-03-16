from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from .views import SignupView
from .forms import LoginForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

app_name = "accounts"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    # Password reset
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            form_class=PasswordResetForm,
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url="/accounts/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class=SetPasswordForm,
            success_url="/accounts/password-reset/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Password change
    path(
        "password-change/",
        PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            form_class=PasswordChangeForm,
            success_url="/accounts/password-change/done/",
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # Add more URL patterns as needed
]
