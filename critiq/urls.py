from django.urls import path
from . import views

app_name = "critiq"

urlpatterns = [
    # Movie URLs
    path("movies/", views.MovieListView.as_view(), name="movie_list"),
    path("movies/create/", views.MovieCreateView.as_view(), name="movie_create"),
    path("movies/<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path(
        "movies/<slug:slug>/update/",
        views.MovieUpdateView.as_view(),
        name="movie_update",
    ),
    path(
        "movies/<slug:slug>/delete/",
        views.MovieDeleteView.as_view(),
        name="movie_delete",
    ),
    # Review URLs
    path(
        "movies/<slug:movie_slug>/review/create/",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "reviews/<slug:slug>/", views.ReviewDetailView.as_view(), name="review_detail"
    ),
    path(
        "reviews/<slug:slug>/update/",
        views.ReviewUpdateView.as_view(),
        name="review_update",
    ),
    path(
        "reviews/<slug:slug>/delete/",
        views.ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    path("my-reviews/", views.UserReviewListView.as_view(), name="user_reviews"),
]
