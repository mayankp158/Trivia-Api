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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'], True)
        self.assertTrue(data['number_of_categories'], True)

    def test_create_question(self):
        """Test POST a new question """

        # Used as header to POST /question
        json_create_question = {
            'question': 'What is your name?',
            'answer': 'Mayank!',
            'category': '1',
            'difficulty': 1
        }

        res = self.client().post('/questions', json=json_create_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'] > 0)

    def test_error_create_question(self):
        """Test POST a new question with missing category """

        # Used as header to POST /question
        json_create_question_error = {
            'question': 'What is your name?',
            'answer': 'Mayank',
            'difficulty': 1
        }

        res = self.client().post('/questions', json=json_create_question_error)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Category can not be blank')

    def test_search_question(self):
        """Test POST to search a question with an existing search term. """

        # Used as header to POST /question
        json_search_question = {
            'searchTerm': 'Taj',
        }

        res = self.client().post('/questions', json=json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['searched_question']) > 0)
        self.assertTrue(data['total_questions'] > 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()