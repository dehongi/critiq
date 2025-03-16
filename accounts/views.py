from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from .models import CustomUser
from .forms import SignupForm

# Create your views here.


class SignupView(View):
    """View for user signup"""

    template_name = "accounts/signup.html"

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")  # Redirect to your home page
        return render(request, self.template_name, {"form": form})
