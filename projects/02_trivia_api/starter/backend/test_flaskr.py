import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """ Get categories """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        category_count = Category.query.count()
        self.assertEqual(data['success'], 1)
        self.assertEqual(len(data['categories']), category_count)
    
    """ Is there any failure case for getting categories? """

    """ Add new question """
    def test_new_question(self):
        new_question = Question(
            question='Test question',
            answer='Test answer',
            category=1,
            difficulty=4
        )
        res = self.client().post('/questions', json=new_question.format())
        data = json.loads(res.data)


        inserted_question = Question.query.filter_by(question='Test question').one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(inserted_question.question, 'Test question')
    
    """ Fail adding new question because of wrong request type """
    def test_new_question_fail(self):
        new_question = Question(
            question='Test question',
            answer='Test answer',
            category=1,
            difficulty=4
        )
        res = self.client().patch('/questions', json=new_question.format())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method not allowed')

    """ Fail adding new question because of empty data """
    def test_new_question_fail_wrong_data(self):
        new_question = Question(
            question='',
            answer='',
            category=1000,
            difficulty=4
        )
        res = self.client().post('/questions', json=new_question.format())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'The request could not be processed')
    
    """ Delete a question """
    def test_question_delete(self):        
        question = Question.query.filter_by(question='Test question').one_or_none()
        res = self.client().delete('/questions/' + str(question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Question has been deleted')

    """ Fail - Delete a question """
    def test_question_delete_fail(self):        
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'The request could not be processed')

    """  Get questions """
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 1)

    """ Fail getting questions """
    def test_get_questions_fail(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'The request could not be processed')

    """ Get category questions """
    def test_get_questions_from_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 1)

    """ Fail getting category questions """
    def test_get_questions_from_category_fail(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'The request could not be processed')

    """ Get a quiz question """
    def test_get_quiz_question(self):
        res = self.client().post('/quizzes', json={'quiz_category': { 'id': 1 }, 'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 1)
    
    """ Fail getting a quiz question """
    def test_get_quiz_question_fail(self):
        res = self.client().post('/quizzes', json={'quiz_category': { 'id': 1000}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'The request could not be processed')
    
    """ Search for questions """
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'what'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 1)

    """ Is there any failure case for searching questions? """

    """ Not found """
    def test_not_found(self):
        res = self.client().get('/categoriesNotFound')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
