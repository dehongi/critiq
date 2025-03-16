from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Avg

from .models import Movie, Review
from .forms import MovieForm, ReviewForm


class MovieListView(ListView):
    """View for listing all movies"""

    model = Movie
    template_name = "critiq/movie_list.html"
    context_object_name = "movies"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add search functionality
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class MovieDetailView(DetailView):
    """View for displaying a single movie with its reviews"""

    model = Movie
    template_name = "critiq/movie_detail.html"
    context_object_name = "movie"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get reviews for this movie
        context["reviews"] = self.object.reviews.all()

        # Check if the user has already reviewed this movie
        if self.request.user.is_authenticated:
            context["user_has_reviewed"] = Review.objects.filter(
                movie=self.object, user=self.request.user
            ).exists()

            # Add review form for users who haven't reviewed yet
            if not context["user_has_reviewed"]:
                context["review_form"] = ReviewForm()

        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new movie"""

    model = Movie
    form_class = MovieForm
    template_name = "critiq/movie_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Movie added successfully!")
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing movie"""

    model = Movie
    form_class = MovieForm
    template_name = "critiq/movie_form.html"
    slug_url_kwarg = "slug"

    def test_func(self):
        movie = self.get_object()
        return self.request.user == movie.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Movie updated successfully!")
        return super().form_valid(form)


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a movie"""

    model = Movie
    template_name = "critiq/movie_confirm_delete.html"
    success_url = reverse_lazy("critiq:movie_list")
    slug_url_kwarg = "slug"

    def test_func(self):
        movie = self.get_object()
        return self.request.user == movie.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Movie deleted successfully!")
        return super().delete(request, *args, **kwargs)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new review"""

    model = Review
    form_class = ReviewForm
    template_name = "critiq/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Get the movie using slug
        self.movie = get_object_or_404(Movie, slug=self.kwargs["movie_slug"])

        # Check if user already reviewed this movie
        if Review.objects.filter(movie=self.movie, user=request.user).exists():
            messages.error(request, "You have already reviewed this movie.")
            return redirect("critiq:movie_detail", slug=self.movie.slug)

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["movie"] = self.movie
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie"] = self.movie
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Review added successfully!")
        return response

    def get_success_url(self):
        return reverse("critiq:movie_detail", kwargs={"slug": self.movie.slug})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing review"""

    model = Review
    form_class = ReviewForm
    template_name = "critiq/review_form.html"
    slug_url_kwarg = "slug"

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie"] = self.object.movie
        context["is_update"] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Review updated successfully!")
        return response


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a review"""

    model = Review
    template_name = "critiq/review_confirm_delete.html"
    slug_url_kwarg = "slug"

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def get_success_url(self):
        return reverse("critiq:movie_detail", kwargs={"slug": self.object.movie.slug})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Review deleted successfully!")
        return super().delete(request, *args, **kwargs)


class ReviewDetailView(DetailView):
    """View for displaying a single review"""

    model = Review
    template_name = "critiq/review_detail.html"
    context_object_name = "review"
    slug_url_kwarg = "slug"


class UserReviewListView(LoginRequiredMixin, ListView):
    """View for listing all reviews by the current user"""

    model = Review
    template_name = "critiq/user_reviews.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
