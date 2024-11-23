from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from waitress import serve
from flask_migrate import Migrate
from flask_restful import Resource, Api, marshal_with, fields
import os


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY")
        )  # default configuration
    else:
        app.config.from_mapping(test_config)

    @app.route("/")
    def index():
        return "<h2>Flask Bookmarks REST API</h2>"

    @app.route("/hello")
    def hello():
        return jsonify({"message": "Hello World"})

    return app


if __name__ == "__main__":
    app = create_app()
    # serve(app, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=8000, debug=True)
