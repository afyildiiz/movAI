from flask import Blueprint, current_app, request, session
from mixpanel import Mixpanel

from movai.services.ai import get_cohere_response
from movai.services.tmdb import get_recommendations, search_title

chat_bp = Blueprint("chat", __name__)

SIMILAR_KEYWORDS = [
    "similar", "like", "recommend", "suggestion", "benzer", "oneri",
    "öneri", "tavsiye", "gibi", "benzeri", "more like",
]


def _wants_recommendations(text):
    lower = text.lower()
    return any(kw in lower for kw in SIMILAR_KEYWORDS)


@chat_bp.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]

    # Check if user is asking for similar titles based on previous search
    if _wants_recommendations(user_input) and session.get("last_tmdb"):
        last = session["last_tmdb"]
        recs = get_recommendations(last["media_type"], last["tmdb_id"])

        if recs:
            rec_lines = []
            for r in recs:
                rec_lines.append(
                    f"- {r['title']} ({r['release_date']}) | "
                    f"TMDB: {r['tmdb_url']} | {r['overview']}"
                )
            recs_text = "\n".join(rec_lines)

            context = (
                f"The user previously searched for: {last['title']} ({last['media_type']})\n"
                f"They are now asking for similar titles.\n\n"
                f"Here are TMDB verified recommendations:\n{recs_text}\n\n"
                f"Present these recommendations using the EXACT TMDB links above. "
                f"Do NOT invent or guess any TMDB URL.\n\n"
                f"User's request: {user_input}"
            )
        else:
            context = user_input
    else:
        # Normal title search
        tmdb_data = search_title(user_input)

        if tmdb_data:
            # Store in session for follow-up recommendation requests
            session["last_tmdb"] = {
                "title": tmdb_data["title"],
                "media_type": tmdb_data["media_type"],
                "tmdb_id": tmdb_data["tmdb_id"],
            }

            context = (
                f"TMDB verified data for this query:\n"
                f"Title: {tmdb_data['title']}\n"
                f"Type: {tmdb_data['media_type']}\n"
                f"Overview: {tmdb_data['overview']}\n"
                f"Release Date: {tmdb_data['release_date']}\n"
                f"Genres: {tmdb_data['genres']}\n"
                f"Production Countries: {tmdb_data['countries']}\n"
                f"TMDB Link: {tmdb_data['tmdb_url']}\n\n"
                f"Use EXACTLY the TMDB Link above. Do NOT invent or guess any TMDB URL.\n\n"
                f"User's request: {user_input}"
            )
        else:
            context = user_input

    response = get_cohere_response(context)

    mp = Mixpanel(current_app.config["MP_PROJECT_KEY"])
    mp.track(
        session["distinct_id"],
        "Conversation Happened",
        {"message": user_input, "path": request.path, "response": response},
    )

    return response
