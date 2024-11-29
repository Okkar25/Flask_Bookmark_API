from flask import Flask, jsonify
from flask_cors import CORS
from waitress import serve
from flask_migrate import Migrate
from flask_restful import Resource, Api, marshal_with, fields
import os
from src.database import db
from src.auth import auth
from src.bookmarks import bookmarks
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Disable to improve performance
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )  # default configuration
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)
    # blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not Found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify(
                {
                    "error": "Something went wrong on server. We are working on it. Please try again in a few moments."
                }
            ),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app


# if __name__ == "__main__":
#     app = create_app()
#     # serve(app, host="0.0.0.0", port=5000)
#     app.run(host="0.0.0.0", port=8000, debug=True)
