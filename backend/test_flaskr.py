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

        self.new_question = {
            'question': 'Nani?',
            'answer': 'Osu',
            'category': 'Science',
            'difficulty': 5
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client()

    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    #def test_get_questions_error(self):
    '''
    def test_delete_question(self):

        res = self.client().delete('/api/questions/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'], 4)
    '''
    #def test_delete_questions_error(self)
    
    def test_post_question(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #def test_post_question_error(self):


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()