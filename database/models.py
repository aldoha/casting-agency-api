import json
import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        create_engine)

load_dotenv('.env')
db = SQLAlchemy()
database_path = os.getenv('DATABASE_URL')


def setup_db(app, database_path=database_path):
    app.config.from_pyfile('settings.py')
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(db.Enum('female', 'male', 'other',
                            name='GenderTypes'), default=None, nullable=True)
    movies = db.relationship('Movie', backref='actor', lazy=True)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
