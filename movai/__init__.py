import uuid

from flask import Flask, session

from movai.config import Config
from movai.extensions import mail
from movai.routes import all_blueprints


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    mail.init_app(app)

    for bp in all_blueprints:
        app.register_blueprint(bp)

    @app.before_request
    def set_anon_id():
        if "distinct_id" not in session:
            session["distinct_id"] = str(uuid.uuid4())

    return app
