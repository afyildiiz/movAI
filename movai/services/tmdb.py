import requests
from flask import current_app

BASE_URL = "https://api.themoviedb.org/3"


def get_movie_details(movie_title):
    api_key = current_app.config["TMDB_API_KEY"]
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": api_key, "query": movie_title, "language": "tr-TR"}

    response = requests.get(search_url, params=params)
    data = response.json()

    if not data["results"]:
        return None

    movie_id = data["results"][0]["id"]
    details_url = f"{BASE_URL}/movie/{movie_id}"
    details = requests.get(
        details_url, params={"api_key": api_key, "language": "tr-TR"}
    ).json()

    return {
        "title": details["title"],
        "overview": details["overview"],
        "release_date": details["release_date"],
        "genres": [g["name"] for g in details["genres"]],
        "production_countries": [c["name"] for c in details["production_countries"]],
        "streaming_platforms": [],
        "tmdb_id": movie_id,
    }


def get_popular_movies():
    api_key = current_app.config["TMDB_API_KEY"]
    popular_url = f"{BASE_URL}/movie/popular"
    params = {"api_key": api_key, "language": "tr-TR"}

    response = requests.get(popular_url, params=params)
    data = response.json()

    return [
        {"title": m["title"], "release_date": m["release_date"]}
        for m in data["results"]
    ]
