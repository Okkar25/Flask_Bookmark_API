from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from waitress import serve
from flask_migrate import Migrate
from flask_restful import Resource, Api, marshal_with, fields
import os
from src.database import db
from src.auth import auth
from src.bookmarks import bookmarks


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
        )  # default configuration
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app


# if __name__ == "__main__":
#     app = create_app()
#     # serve(app, host="0.0.0.0", port=5000)
#     app.run(host="0.0.0.0", port=8000, debug=True)
