import requests
from flask import current_app

BASE_URL = "https://api.themoviedb.org/3"


def search_title(query):
    """Search TMDB for a movie or TV show by name. Returns details dict or None."""
    api_key = current_app.config["TMDB_API_KEY"]

    # Try multi-search (covers movies + TV)
    resp = requests.get(
        f"{BASE_URL}/search/multi",
        params={"api_key": api_key, "query": query, "language": "en-US"},
    ).json()

    results = [
        r for r in resp.get("results", [])
        if r.get("media_type") in ("movie", "tv")
    ]
    if not results:
        return None

    hit = results[0]
    media_type = hit["media_type"]
    item_id = hit["id"]

    # Fetch full details
    details = requests.get(
        f"{BASE_URL}/{media_type}/{item_id}",
        params={"api_key": api_key, "language": "en-US"},
    ).json()

    title = details.get("title") or details.get("name", "")
    overview = details.get("overview", "")
    release_date = details.get("release_date") or details.get("first_air_date", "")
    genres = ", ".join(g["name"] for g in details.get("genres", []))
    countries = ", ".join(
        c["name"] for c in details.get("production_countries",
                                        details.get("origin_country", []))
    )
    # origin_country is a list of ISO codes for TV, handle gracefully
    if not countries and details.get("origin_country"):
        countries = ", ".join(details["origin_country"])

    tmdb_url = f"https://www.themoviedb.org/{media_type}/{item_id}"

    return {
        "title": title,
        "overview": overview,
        "release_date": release_date,
        "genres": genres,
        "countries": countries,
        "tmdb_url": tmdb_url,
        "media_type": media_type,
        "tmdb_id": item_id,
    }


def get_recommendations(media_type, item_id, limit=6):
    """Fetch similar/recommended titles from TMDB with verified links."""
    api_key = current_app.config["TMDB_API_KEY"]

    resp = requests.get(
        f"{BASE_URL}/{media_type}/{item_id}/recommendations",
        params={"api_key": api_key, "language": "en-US"},
    ).json()

    results = resp.get("results", [])[:limit]
    recs = []
    for r in results:
        rid = r["id"]
        rtype = media_type
        title = r.get("title") or r.get("name", "")
        date = r.get("release_date") or r.get("first_air_date", "")
        genres = ", ".join(
            str(gid) for gid in r.get("genre_ids", [])
        )
        overview = r.get("overview", "")[:150]
        tmdb_url = f"https://www.themoviedb.org/{rtype}/{rid}"
        recs.append({
            "title": title,
            "release_date": date,
            "overview": overview,
            "tmdb_url": tmdb_url,
        })
    return recs


def get_popular_movies():
    api_key = current_app.config["TMDB_API_KEY"]
    resp = requests.get(
        f"{BASE_URL}/movie/popular",
        params={"api_key": api_key, "language": "en-US"},
    ).json()

    return [
        {"title": m["title"], "release_date": m["release_date"]}
        for m in resp.get("results", [])
    ]
