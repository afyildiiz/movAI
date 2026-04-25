from flask import Blueprint, request, session
from mixpanel import Mixpanel

from movai.services.ai import get_cohere_response

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/get_response", methods=["POST"])
def get_response():
    from flask import current_app

    user_input = request.form["user_input"]

    prompt = f"""
        You are a movie and TV show chatbot. Users will ask you for movie or TV show titles, and you will provide them with relevant information using the TMDB API. You can also list popular movies and the best movies by genre.

        Respond to the user in an understanding manner and perhaps suggest another search.

        User's request: {user_input}

        Use the TMDB API to provide an appropriate response.

        If the user requests information about a movie or TV series, first find the movie or TV series using the TMDB API. Then, make sure it contains the following information and please structure your response under the following subheadings:
        * Movie Details
        * Title:
        * Overview:
        * Release Date:
        * Genres:
        * Production Countries:
        * TMDB Link: (in the format <a href="https://www.themoviedb.org/movie/<movie_id>" target="_blank">TMDB Page</a>)
        * Streaming Platforms: (if exist, must be)
        If the user requests popular movies or the best movies by a specific genre, provide the relevant lists.

        If you don't understand the user's request, politely ask for more information or clarification.

        You should make the html view as follows and never break this rule:

            <h3>Movie Details</h3>
            </br>
        <ul>
            <li><strong>Title:</strong> Narcos</li>
            </br>
            <li><strong>Overview:</strong> 'Narcos' is an exciting and gritty crime drama series...</li>
            </br>
            <li><strong>Release Date:</strong> August 28, 2015</li>
            </br>
            <li><strong>Genres:</strong> Crime, Drama, Biography</li>
            </br>
            <li><strong>Production Countries:</strong> United States, Colombia</li>
            </br>
            <li><strong>TMDB Link:</strong> <a href="https://www.themoviedb.org/movie/63351" target="_blank">TMDB Page</a> </li>
            </br>
            <li><strong>Streaming Platforms:</strong> Netflix, Disney+ </li>
            </br>

        </ul>

        <h2>Popular Movies:</h2>
        </br>
        <ul>
            <li><strong>Inception</strong><br />Release Date: July 16, 2010</li>
            </br>
            <li><strong>The Dark Knight</strong><br />Release Date: July 18, 2008</li>
            </br>
        </ul>
    """

    response = get_cohere_response(prompt)

    mp = Mixpanel(current_app.config["MP_PROJECT_KEY"])
    mp.track(
        session["distinct_id"],
        "Conversation Happened",
        {"message": user_input, "path": request.path, "response": response},
    )

    return response
