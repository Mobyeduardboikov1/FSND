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
        self.database_path = "postgres://{}/{}".format('eduardnix:2wsx3edc@localhost:5432', self.database_name)
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
    
    """ Delete a question """
    def test_question_delete(self):        
        question = Question.query.filter_by(question='Test question').one_or_none()
        res = self.client().delete('/questions/' + str(question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Question has been deleted')

    """ Not found """
    def test_not_found(self):
        res = self.client().get('/categoriesNotFound')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()