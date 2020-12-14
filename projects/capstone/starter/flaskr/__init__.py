import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from auth import AuthError, requires_auth
from models import *

print("Name = " + __name__)
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route("/test", methods=["GET"])
  def test_route():
    print("Hey, test route hit!")

    return "Hey!"

  # Actors
  @app.route("/actors", methods=["GET"])
  @requires_auth("view:actors")
  def actors(payload):
    actors = [actor.format() for actor in Actor.query.all()]
    return jsonify({'success': 1, 'actors': actors})

  # Add an actor
  @app.route("/actors", methods=["POST"])
  @requires_auth("add:actor")
  def actorAdd(payload):
    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if len(name) == 0:
      abort(422)

    actor = Actor(
        name=name,
        age=age,
        gender=gender
      )
    actor.insert()

    result = {
        'success': 1,
        'message': 'Actor has been added',
        'id': actor.id
        }
    return jsonify(result)

  # Update an actor
  @app.route("/actors/<int:actor_id>", methods=["PATCH"])
  @requires_auth("update:actor")
  def updateActor(payload, actor_id):
      body = request.get_json()
      actor = Actor.query.get(actor_id)

      if actor is None:
        abort(404)

      name = body.get('name', actor.name)
      age = body.get('age', actor.age)
      gender = body.get('gender', actor.gender)


      
      if len(name) == 0:
        abort(422)

      actor.name = name
      actor.age = age
      actor.gender = gender
      actor.update()

      result = {
          'success': 1,
          'message': 'Actor has been updated',
          'id': actor.id
          }
      return jsonify(result)
  # Delete an actor
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth("delete:actor")
  def deleteActor(payload, actor_id):
      actor = Actor.query.get(actor_id)
      result = {
          'success': 1,
          'message': 'Actor has been deleted',
          'id': actor_id}
      status_code = 200
      if actor is not None:
          actor.delete()
      else:
          abort(422)

      return jsonify(result)
      
  # Movies
  @app.route("/movies", methods=["GET"])
  @requires_auth("view:movies")
  def movies(payload):
    movies = [movie.format() for movie in Movie.query.all()]
    return jsonify({'success': 1, 'movies': movies})

  # Add a movie
  @app.route("/movies", methods=["POST"])
  @requires_auth("add:movie")
  def movieAdd(payload):
    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release_date')
    if len(title) == 0 or release_date is None:
      abort(422)

    movie = Movie(
        title=title,
        release_date=release_date
        )
    movie.insert()

    result = {
        'success': 1,
        'message': 'Movie has been added',
        'id': movie.id
        }
    return jsonify(result)


  # Update a movie
  @app.route("/movies/<int:movie_id>", methods=["PATCH"])
  @requires_auth("update:movie")
  def updateMovie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    if (movie is None):
      abort(404)
    body = request.get_json()
    title = body.get('title', movie.title)
    release_date = body.get('release_date', movie.release_date)

    if len(title) == 0 or release_date is None:
      abort(422)

    movie.title = title
    movie.release_date = release_date
    movie.update()

    result = {
        'success': 1,
        'message': 'Movie has been updated',
        'id': movie.id
        }
    return jsonify(result)

  # Delete a movie
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth("delete:movie")
  def deleteMovie(payload, movie_id):
      movie = Movie.query.get(movie_id)
      result = {
          'success': 1,
          'message': 'Movie has been deleted',
          'id': movie_id}
      status_code = 200
      if movie is not None:
          movie.delete()
      else:
          abort(422)

      return jsonify(result)
  ## Error Handling
  '''
  Example error handling for unprocessable entity
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'message': 'Resource was not found.',
          'error': 404
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'message': 'The request could not be processed',
          'error': 422
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'message': 'Bad request',
          'error': 400
      }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success': False,
          'message': 'Method not allowed',
          'error': 405
      }), 405

  @app.errorhandler(500)
  def internal_error(error):
      return jsonify({
          'success': False,
          'message': 'Internal server error',
          'error': 500
      }), 500

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)