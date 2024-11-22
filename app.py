from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from waitress import serve
from flask_migrate import Migrate
from flask_restful import Resource, Api, marshal_with, fields

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return "<h2>Flask Bookmarks REST API</h2>"


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello World"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    # serve(app, host="0.0.0.0", port=8000, debug=True)
