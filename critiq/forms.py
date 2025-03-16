from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    """Form for creating and updating movies"""

    class Meta:
        model = Movie
        fields = ["title", "release_year", "director", "synopsis", "poster"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Movie title"}
            ),
            "release_year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Release year"}
            ),
            "director": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Director name"}
            ),
            "synopsis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Movie synopsis",
                    "rows": 5,
                }
            ),
            "poster": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        movie = super().save(commit=False)
        if self.user:
            movie.user = self.user
        if commit:
            movie.save()
        return movie


class ReviewForm(forms.ModelForm):
    """Form for creating and updating reviews"""

    class Meta:
        model = Review
        fields = ["title", "content", "rating"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Review title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your review here",
                    "rows": 6,
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Rating (1-10)",
                    "min": 1,
                    "max": 10,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.movie = kwargs.pop("movie", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        review = super().save(commit=False)
        if self.user:
            review.user = self.user
        if self.movie:
            review.movie = self.movie
        if commit:
            review.save()
        return review
