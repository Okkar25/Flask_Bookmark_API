from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
)
import validators
from src.database import db, User

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# @auth.route("/register", methods=["POST"])
@auth.post("/register")
def register():
    username = request.json["username"]  # request.form.get()
    email = request.json["email"]
    password = request.json["password"]

    # data validation
    if len(password) < 6:
        return (
            jsonify({"error": "Password must be longer than 6 characters."}),
            HTTP_400_BAD_REQUEST,
        )

    if len(username) < 3:
        return (
            jsonify({"error": "Username must be longer than 3 characters."}),
            HTTP_400_BAD_REQUEST,
        )

    if not username.isalnum() or " " in username:
        return (
            jsonify({"error": "username should be alphanumeric with no spaces"}),
            HTTP_400_BAD_REQUEST,
        )

    # use validators package
    if not validators.email(email):
        return (
            jsonify({"error": "You must enter a valid email address."}),
            HTTP_400_BAD_REQUEST,
        )

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "This email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "This username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {"message": "User created", "user": {"username": username, "email": email}}
        ),
        HTTP_201_CREATED,
    )


@auth.route("/me", methods=["GET"])
def me():
    return {"user": "me"}
