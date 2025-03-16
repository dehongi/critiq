from django import forms
from .models import CustomUser
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm as DjangoPasswordResetForm,
    SetPasswordForm as DjangoSetPasswordForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)


class SignupForm(forms.ModelForm):
    """Form for user signup"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Form for user login with Bootstrap 5 styling"""

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email", "autofocus": True}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )

    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    error_messages = {
        "invalid_login": "Please enter a correct email and password. Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }


class PasswordResetForm(DjangoPasswordResetForm):
    """Form for password reset with Bootstrap 5 styling"""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email address"}
        )
    )


class SetPasswordForm(DjangoSetPasswordForm):
    """Form for setting a new password with Bootstrap 5 styling"""

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        ),
    )


class PasswordChangeForm(DjangoPasswordChangeForm):
    """Form for changing password with Bootstrap 5 styling"""

    old_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Current password"}
        ),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        ),
    )
