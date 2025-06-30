from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Movie, SavedReview, UserMoviePlaylist


@login_required
def saved_reviews(request):
    saved = (
        SavedReview.objects.filter(user=request.user)
        .select_related("review", "movie")
        .order_by("-saved_at")
    )
    return render(request, "saved_reviews.html", {"saved_reviews": saved})


@login_required
def playlist(request):
    saved = (
        SavedReview.objects.filter(user=request.user)
        .select_related("review", "movie")
        .order_by("-saved_at")
    )
    movies = (
        UserMoviePlaylist.objects.filter(user=request.user)
        .select_related("movie")
        .order_by("-added_at")
    )
    return render(request, "playlist.html", {"saved_reviews": saved, "movies": movies})


@login_required
def add_to_playlist(request, movie_id):
    movie_obj, _ = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            "title": request.GET.get("title", ""),
            "poster_url": request.GET.get("poster_url", ""),
            "release_date": request.GET.get("release_date"),
            "rating": request.GET.get("rating", 0.0),
        },
    )
    UserMoviePlaylist.objects.get_or_create(user=request.user, movie=movie_obj)
    messages.success(request, f"{movie_obj.title} added to your playlist!")
    return redirect("playlist")


@login_required
def remove_from_playlist(request, movie_id):
    UserMoviePlaylist.objects.filter(
        user=request.user, movie__tmdb_id=movie_id
    ).delete()
    messages.success(request, "Movie removed from your playlist.")
    return redirect("playlist")
