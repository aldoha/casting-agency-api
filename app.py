import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from auth.auth import AuthError, requires_auth
from database.models import Actor, Movie, setup_db

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response


# Routes

@app.route('/')
def index():
    return "Casting Agency API"


@app.route('/movies')
@requires_auth(permission='get:movies')
def receive_movies(payload):
    data = Movie.query.all()
    movies = [movie.format() for movie in data]
    return jsonify({
        "success": True, "movies": movies
    })


@app.route('/actors')
@requires_auth(permission='get:actors')
def receive_actors(payload):
    data = Actor.query.all()
    actors = [actor.format() for actor in data]
    return jsonify({
        "success": True, "actors": actors
    })


@app.route('/movies', methods=['POST'])
@requires_auth(permission='post:movies')
def create_new_movie(payload):
    body = request.get_json()
    movie_id = body.get('id', None)
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    if title is not None and title != '':
        movie = Movie(id=movie_id, title=title, release_date=release_date)
        movie.insert()
    else:
        abort(400)

    return jsonify({
        "success": True, "movie": movie.format()
    })


@app.route('/actors', methods=['POST'])
@requires_auth(permission='post:actors')
def create_new_actor(payload):
    body = request.get_json()
    actor_id = body.get('id', None)
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    if name != '' and name is not None:
        actor = Actor(id=actor_id, name=name, gender=gender, age=age)
        actor.insert()
    else:
        abort(400)

    return jsonify({
        "success": True, "actor": actor.format()
    })


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth(permission='patch:movies')
def edit_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    body = request.get_json()
    new_title = body.get('title', None)
    if new_title != '' and new_title is not None:
        movie.title = new_title

    new_release_date = body.get('release_date', None)
    if new_release_date != '' and new_release_date is not None:
        movie.release_date = new_release_date
    movie.update()

    return jsonify({
        "success": True, "movie": movie.format()
    })


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth(permission='patch:actors')
def edit_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    body = request.get_json()
    new_name = body.get('name', None)
    if new_name != '' and new_name is not None:
        actor.name = new_name

    new_age = body.get('age', None)
    if new_age != '' and new_age is not None:
        actor.age = new_age

    new_gender = body.get('gender', None)
    if new_gender != '' and new_gender is not None:
        actor.gender = new_gender

    new_movie_connection = body.get('movie_id', None)
    if new_movie_connection != '' and new_movie_connection is not None:
        actor.movie_id = new_movie_connection
    actor.update()

    return jsonify({
        "success": True, "actor": actor.format()
    })


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth(permission='delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    actor.delete()

    return jsonify({
        "success": True, "deleted": actor.format()
    })


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth(permission='delete:movies')
def delete_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    movie.delete()

    return jsonify({
        "success": True, "deleted": movie.format()
    })


# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
