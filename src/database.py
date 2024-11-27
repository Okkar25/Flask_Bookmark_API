from flask_sqlalchemy import SQLAlchemy
from enum import unique
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())  # automatic
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship("Bookmark", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"User >>> {self.username}"


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(6), nullable=False)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # user = User()
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        SHORT_URL_LENGTH = 6
        # picked_chars = "".join(random.choices(characters, k=SHORT_URL_LENGTH))

        # Check if the short URL is unique
        # checking if the generated short_url already exist in database
        # link = self.query.filter_by(short_url=picked_chars).first()
        # if link:
        #     self.generate_short_characters()
        # else:
        #     return picked_chars

        while True:
            picked_chars = "".join(random.choices(characters, k=SHORT_URL_LENGTH))

            # Check if the short URL is unique
            # checking if the generated short_url already exist in database
            if not self.query.filter_by(short_url=picked_chars).first():
                return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.short_url:
            self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return f"Bookmark >>> {self.url}"


# Foreign Key => Primary Key
