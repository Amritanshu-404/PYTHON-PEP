import requests
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.conf import settings

from ..models import Review, Movie, SavedReview, UserMoviePlaylist

TMDB_API_KEY = settings.TMDB_API_KEY


@login_required
def submit_review(request, movie_id):
    if request.method == "POST":
        review_text = request.POST.get("review", "").strip()
        rating = request.POST.get("rating")

        try:
            rating = float(rating)
            movie_id_int = int(movie_id)
        except (TypeError, ValueError):
            messages.error(request, "Invalid input.")
            return redirect("entertainment")

        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        movie_resp = requests.get(movie_url).json()

        movie_obj, _ = Movie.objects.get_or_create(
            tmdb_id=movie_id_int,
            defaults={
                "title": movie_resp.get("title", ""),
                "poster_url": (
                    f"https://image.tmdb.org/t/p/w500{movie_resp['poster_path']}"
                    if movie_resp.get("poster_path")
                    else ""
                ),
                "release_date": movie_resp.get("release_date"),
                "rating": movie_resp.get("vote_average", 0.0),
            },
        )

        if review_text and rating > 0:
            try:
                review = Review.objects.create(
                    user=request.user,
                    movie_id=movie_id_int,
                    review_text=review_text,
                    rating=rating,
                )
                UserMoviePlaylist.objects.get_or_create(
                    user=request.user, movie=movie_obj
                )
                SavedReview.objects.get_or_create(
                    user=request.user, movie=movie_obj, review=review
                )
                messages.success(request, "Review submitted successfully!")
            except IntegrityError:
                messages.error(
                    request, "You have already submitted a review for this movie."
                )
            return redirect("movie_detail", movie_id=movie_id)

        messages.error(request, "Please enter a valid review and rating.")
        return redirect("movie_detail", movie_id=movie_id)


@login_required
def save_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie = Movie.objects.filter(tmdb_id=review.movie_id).first()

    if not movie:
        url = f"https://api.themoviedb.org/3/movie/{review.movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        resp = requests.get(url)
        if resp.status_code != 200:
            messages.error(request, "Could not fetch movie data to save review.")
            return redirect("movie_detail", movie_id=review.movie_id)

        data = resp.json()
        movie = Movie.objects.create(
            tmdb_id=review.movie_id,
            title=data.get("title", ""),
            poster_url=(
                f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
                if data.get("poster_path")
                else ""
            ),
            release_date=data.get("release_date"),
            rating=data.get("vote_average", 0.0),
        )

    SavedReview.objects.get_or_create(user=request.user, movie=movie, review=review)
    messages.success(request, "Review saved to your playlist!")
    return redirect("saved_reviews")
