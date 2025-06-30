from django.urls import path

from .views.auth_views import signup_view, login_view, logout_view
from .views.movie_views import popular_movies, entertainment_view
from .views.movie_detail_views import movie_detail
from .views.review_views import submit_review, save_review
from .views.playlist_views import (
    saved_reviews,
    playlist,
    add_to_playlist,
    remove_from_playlist,
)

urlpatterns = [
    path("", popular_movies, name="popular_movies"),  # Home Page
    path("entertainment/", entertainment_view, name="entertainment"),
    path("signup/", signup_view, name="signup"),  # Signup Page
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("movie/<int:movie_id>/", movie_detail, name="movie_detail"),
    path("movie/<int:movie_id>/submit_review/", submit_review, name="submit_review"),
    path("save_review/<int:review_id>/", save_review, name="save_review"),
    path("saved_reviews/", saved_reviews, name="saved_reviews"),
    path("playlist/", playlist, name="playlist"),
    path("add_to_playlist/<int:movie_id>/", add_to_playlist, name="add_to_playlist"),
    path(
        "remove_from_playlist/<int:movie_id>/",
        remove_from_playlist,
        name="remove_from_playlist",
    ),
]
