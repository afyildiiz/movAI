## **MovAI - Your Artificial Intelligence Powered Movie and TV Series Guide**

## Website Link: https://movai-production.up.railway.app/

MovAI is an AI-powered chatbot application that makes it easy for you to explore the world of movies and TV series. Using The Movie Database (TMDb) API, it accesses a large database of movies and TV shows and provides you with personalized recommendations, detailed information and lists of popular content.

## **Features**

* Movie & TV Series Recommendations:** Provides customized recommendations based on genre, actor, director or any keyword.
* Detailed Information:** Provides detailed information about a movie or TV series such as title, synopsis, release date, genres, production countries, TMDb link and streaming platforms.
* Popular & Best Lists:** Lists current popular movies or the best movies in a particular genre.
* **User Friendly Interface:** The chat-based interface allows you to ask questions using natural language and get answers quickly.

## **Technologies**

**Flask:** Python based web framework, used to create the backend of the application.
* TMDb API:** Used to provide movie and series data.
** **Cohere API:** Used for natural language processing (NLP) capabilities (if you use it)
* HTML, CSS, JavaScript:** Used to create the frontend and user interface of the application.
** **Waitress (optional):** Can be used to run the Flask application in production environment.

## **Installation**

1. **Clone the Project Repo:**
   ```bash
   git clone https://github.com/afyildiiz/movAI.git
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Your TMDb API Key:**
   * Go to The Movie Database (TMDb) website and create an account.
   * Generate your API key and save it as an environment variable called `TMDB_API_KEY`.

4. **Get your Cohere API Key (if you are using it):**
   * Go to the Cohere website and create an account.
   * Generate your API key and save it as an environment variable called `COHERE_API_KEY`.

5. **Run the Application:**
   ```bash
   # For development environment:
   flask run

   # For Production environment (using Waitress):
   waitress-serve --port=8000 app:app
   ```

## **Usage**

1. Open the app in your browser.
2. Ask the chatbot interface questions about movie or series names, genres, actors or directors.
3. MovAI will provide you with relevant information or suggestions.

**Sample Requests**

* “Show the synopsis of the movie Inception.”
* “What are the best movies in the science fiction genre?”
* “List the movies starring Leonardo DiCaprio.”
* “Suggest a comedy movie.”