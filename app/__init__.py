
from flask import Flask
from dotenv import load_dotenv

from config import Config
from app.extensions import db


def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Load configuration settings.
    app.config.from_object(Config)

    # Connect SQLAlchemy to this Flask application.
    db.init_app(app)

    # Register website routes.
    from app.routes import main
    app.register_blueprint(main)

    return app
