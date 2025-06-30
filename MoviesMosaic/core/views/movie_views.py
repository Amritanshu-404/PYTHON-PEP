import requests
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY


def popular_movies(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page=1"
    response = requests.get(url)

    if response.status_code != 200:
        messages.error(request, "TMDB API Error: Could not load movies.")
        return render(request, "Home.html", {"movies": []})

    data = response.json()
    movies = [
        {
            "id": m["id"],
            "title": m["title"],
            "poster_url": (
                f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
                if m["poster_path"]
                else ""
            ),
            "rating": round(m.get("vote_average", 0), 1),
            "release_date": m.get("release_date", "N/A"),
        }
        for m in data.get("results", [])
    ]
    return render(request, "Home.html", {"movies": movies})


def entertainment_view(request):
    query = request.GET.get("query")
    filter_type = request.GET.get("filter")
    page = max(int(request.GET.get("page", 1)), 1)

    if query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&include_adult=false&page={page}"
    else:
        endpoint = "now_playing" if filter_type == "latest" else "popular"
        url = f"https://api.themoviedb.org/3/movie/{endpoint}?api_key={TMDB_API_KEY}&language=en-US&page={page}&include_adult=false"

    response = requests.get(url)
    if response.status_code != 200:
        messages.error(request, "TMDB API Error: Could not load movies.")
        return render(
            request,
            "entertainment.html",
            {
                "movies": [],
                "query": query or "",
                "filter": filter_type or "popular",
                "page": page,
            },
        )

    data = response.json()
    results = data.get("results", [])
    movies = [
        m
        for m in results
        if m.get("vote_average", 0) >= 4
        and not m.get("adult", False)
        and m.get("poster_path")
    ]

    if query:
        q_lower = query.lower()
        movies.sort(
            key=lambda m: (
                q_lower not in m.get("title", "").lower(),
                -m.get("vote_average", 0),
            )
        )

    movies = [
        {
            "id": m["id"],
            "title": m["title"],
            "poster_url": f"https://image.tmdb.org/t/p/w500{m['poster_path']}",
            "rating": round(m.get("vote_average", 0), 1),
            "release_date": m.get("release_date", "N/A"),
        }
        for m in movies
    ]

    return render(
        request,
        "entertainment.html",
        {
            "movies": movies,
            "query": query or "",
            "filter": filter_type or "popular",
            "page": page,
            "total_pages": data.get("total_pages", 1),
        },
    )
