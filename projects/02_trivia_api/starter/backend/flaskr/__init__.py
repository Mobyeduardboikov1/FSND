import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exc
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Mehotds', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    return response

  """ Get all categories """
  @app.route('/categories', methods=['GET'])
  def categories():    
    categories = {}
    for category in Category.query.order_by(Category.id).all():
      categories[category.id] = category.type
    return jsonify({
      'success': 1,
      'categories': categories
    })

  """ Get all questions. If out of bounds it will return an empty list """
  @app.route('/questions', methods=['GET'])
  def questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in Question.query.order_by(Question.id).all()]
    questions = questions[start:end]
    categories = {}
    for category in Category.query.order_by(Category.id).all():
      categories[category.id] = category.type
    return jsonify({
      'success': 1,
      'questions': questions[start:end],
      'categories': categories,
      'totalQuestions': len(questions),
      'currentCategory': categories[1]
      })
 

  """ Delete a question """
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def deleteQuestion(question_id):
    question = Question.query.get(question_id)
    question.delete()

    result = {'success': 1, 'message': 'Question has been deleted'}
    return jsonify(result)

  """ Add new question """
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()
    question = Question(
      question = body.get('question'),
      category = body.get('category'),
      answer = body.get('answer'),
      difficulty = body.get('difficulty')
    )
    
    question.insert()

    result = {'success': 1, 'message': 'Question has been added'}
    return jsonify(result)
   

  """ Search for questions """
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    searchTerm = body.get('searchTerm')
    questions = [question.format() for question in Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()]
    total_questions = len(questions)
    current_category = 0
    if total_questions > 0:
      current_category = questions[0]['category']
    return jsonify({
      'questions': questions,
      'total_questions': total_questions,
      'current_category': current_category
      })

  """ Get question from a specific category """
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def category_questions(category_id):
    questions = [question.format() for question in Question.query.filter_by(category = category_id).order_by(Question.id).all()]
    return jsonify({
      'questions': questions,
      'total_questions': len(questions),
      'current_category': category_id
    })

  """ Post quiz answer """
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    body = request.get_json()
    category_id = body.get('current_category', None)
    previous_questions = body.get('previous_questions', [])
    if category_id is not None:
      question = Question.query.filter_by(category = category_id).filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
    else:
      question = questions = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()


    return jsonify({
      'question': question.format(),
      'current_category': category_id
    })

  
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

    