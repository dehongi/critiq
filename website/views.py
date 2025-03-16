from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django import forms

# Create your views here.


class HomeView(TemplateView):
    """View for the home page"""

    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add featured movies, recent reviews, etc. here
        context["featured_section_title"] = "Featured Movies"
        return context


class AboutView(TemplateView):
    """View for the about page"""

    template_name = "website/about.html"


class ContactForm(forms.Form):
    """Form for contact page"""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        )
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your Message", "rows": 5}
        )
    )


class ContactView(FormView):
    """View for the contact page"""

    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = "/contact/"  # Redirect back to contact page after submission

    def form_valid(self, form):
        # Process the form data (e.g., send email)
        # This is where you would typically send an email with the form data
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        # For now, just add a success message
        messages.success(
            self.request, "Thank you for your message! We'll get back to you soon."
        )

        # You could implement email sending here:
        # send_mail(
        #     f"Contact Form: {subject}",
        #     f"From: {name} <{email}>\n\n{message}",
        #     email,
        #     ["your-email@example.com"],
        #     fail_silently=False,
        # )

        return super().form_valid(form)


class TermsView(TemplateView):
    """View for the terms of service page"""

    template_name = "website/terms.html"


class PrivacyView(TemplateView):
    """View for the privacy policy page"""

    template_name = "website/privacy.html"


def faq(request):
    """View for the FAQ page"""
    return render(request, "website/faq.html")


def help_center(request):
    """View for the Help Center page"""
    return render(request, "website/help.html")
