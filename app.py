import os
import requests
import cohere
from flask import Flask, request, render_template
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
load_dotenv()

# SMTP AYARLARI
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

tmdb_api_key = os.environ.get('TMDB_API_KEY')
cohere_api_key = os.environ.get('COHERE_API_KEY')

co = cohere.Client(cohere_api_key)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['message']

        # eposta mesajını oluştur
        msg = Message('Yeni İletişim Formu Gönderimi', sender=email, recipients=[os.environ.get('MAIL_USERNAME')])
        msg.body = f"İsim: {name}\nE-posta: {email}\n\n {comment}"

        # E-postayı gönder
        mail.send(msg)

        feedback= "Message has been sent!"
        return render_template('contact.html', data=feedback)  # data değişkenini gönder
    
    return render_template("contact.html")


def get_movie_details(movie_title):
    """tmdb api'sinden film detaylarını alma"""

    base_url = "https://api.themoviedb.org/3"
    search_url = f"{base_url}/search/movie"
    params = {
        "api_key": tmdb_api_key,
        "query": movie_title,
        "language": "tr-TR"
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if data["results"]:
        movie_id = data["results"][0]["id"]
        details_url = f"{base_url}/movie/{movie_id}"
        response = requests.get(details_url, params={"api_key": tmdb_api_key, "language": "tr-TR"})
        details = response.json()

        title = details["title"]
        overview = details["overview"]
        release_date = details["release_date"]
        genres = [genre["name"] for genre in details["genres"]]
        production_countries = [country["name"] for country in details["production_countries"]]

        # streaming platformlarını almak için ayrı bir çağrı yapma
        streaming_platforms = [] 

        return {
            "title": title,
            "overview": overview,
            "release_date": release_date,
            "genres": genres,
            "production_countries": production_countries,
            "streaming_platforms": streaming_platforms,
            "tmdb_id": movie_id 
        }
    else:
        return None

def get_popular_movies():
    """tmdb api'sinden popüler filmleri alma"""

    base_url = "https://api.themoviedb.org/3"
    popular_url = f"{base_url}/movie/popular"
    params = {
        "api_key": tmdb_api_key,
        "language": "tr-TR"
    }

    response = requests.get(popular_url, params=params)
    data = response.json()

    popular_movies = []
    for movie in data["results"]:
        popular_movies.append({
            "title": movie["title"],
            "release_date": movie["release_date"]
        })

    return popular_movies

def get_top_rated_movies_by_genre(genre):
    """tmdb api'sinden belirli bir türe göre en iyi filmleri alma"""

    # ilk olarak, tür adını tür idsine dönüştürecegiz

    top_rated_movies = [] 
    return top_rated_movies

def get_cohere_response(prompt):
    """Cohere API'sinden yanıt alma"""

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=450,
        temperature=0.7,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=[],
        return_likelihoods='NONE'
    )

    return response.generations[0].text.strip()

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]

    # Cohere'a gönderilecek promptu oluştur
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

    return response 


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)