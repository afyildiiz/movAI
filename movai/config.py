import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("MP_API_SECRET", "dev-secret-key")

    # SMTP
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # External APIs
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

    # Mixpanel
    MP_PROJECT_KEY = os.environ.get("MP_PROJECT_KEY")
