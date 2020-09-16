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
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Mehotds',
            'GET, POST, PUT, PATCH, DELETE, OPTIONS')
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
        questions = [question.format()
                     for question in Question.query.order_by(Question.id).all()]
        question_count = len(questions)
        current_questions = questions[start:end]
        if (len(current_questions) == 0):
            abort(422)
        categories = {}
        for category in Category.query.order_by(Category.id).all():
            categories[category.id] = category.type
        return jsonify({
            'success': 1,
            'questions': current_questions,
            'categories': categories,
            'totalQuestions': question_count,
            'currentCategory': categories[1]
        })

    """ Delete a question """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        question = Question.query.get(question_id)
        result = {
            'success': 1,
            'message': 'Question has been deleted',
            'id': question_id}
        status_code = 200
        if question is not None:
            question.delete()
        else:
            abort(422)

        return jsonify(result)

    """ Add new question """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        category_id = body.get('category')
        question_text = body.get('question')
        question_answer = body.get('answer')
        category = Category.query.get(category_id)
        if category is None or len(question_text) == 0 or len(question_answer) == 0:
          abort(422)

        question = Question(
            question=question_text,
            category=category_id,
            answer=question_answer,
            difficulty=body.get('difficulty')
        )
        question.insert()

        result = {
            'success': 1,
            'message': 'Question has been added',
            'id': question.id}
        return jsonify(result)

    """ Search for questions """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        searchTerm = body.get('searchTerm')
        questions = [question.format() for question in Question.query.filter(
            Question.question.ilike('%{}%'.format(searchTerm))).all()]
        total_questions = len(questions)
        current_category = 0
        if total_questions > 0:
            current_category = questions[0]['category']
        return jsonify({
            'questions': questions,
            'total_questions': total_questions,
            'current_category': current_category,
            'success': 1
        })

    """ Get question from a specific category """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def category_questions(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(422)

        questions = [
            question.format() for question in Question.query.filter_by(
                category=str(category_id)).order_by(
                Question.id).all()]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id,
            'success': 1
        })

    """ Get quiz question """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        quiz_category = body.get('quiz_category', None)
        category = Category.query.get(quiz_category['id'])
        if category is None and quiz_category['id'] != 0:
            abort(422)
        category_id = quiz_category['id']
        
        previous_questions = body.get('previous_questions', [])
        if category_id is not None and int(category_id) > 0:
            question = Question.query.filter_by(
                category=category_id).filter(
                Question.id.notin_(previous_questions)).order_by(
                func.random()).first()
        else:
            question = questions = Question.query.filter(
                Question.id.notin_(previous_questions)).order_by(
                func.random()).first()

        return jsonify({
            'question': question.format() if question is not None else False,
            'current_category': category_id,
            'success': 1
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
