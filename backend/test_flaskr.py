import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres@{}/{}".format(
            'localhost:5432',
            self.database_name
            )
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question":
            "Which position player holds the NFL record for most touchdowns?",
            "answer": "Jerry Rice",
            "category": "6",
            "difficulty": 3
        }

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
    Done
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    '''
    GET Methods
    '''
    # Test get all categories
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    # Test a request for bad url returns 404 message
    def test_get_categories_error(self):
        res = self.client().get('/api/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test get all Questions
    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    # Test request for questions page that does not exist returns 404
    def test_get_questions_error(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    '''
    POST Methods
    '''
    # Test creating a new question
    def test_post_question(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

        # Delete the question after running test
        question = Question.query.order_by(Question.id.desc()).first()
        question.delete()

    # Test creating a question with no question/answer attribute
    def test_post_question_error(self):
        bad_question = {
            'question': '',
            'answer': '',
            'category': 1,
            'difficulty': 2
        }
        res = self.client().post('/api/questions', json=bad_question)
        data = json.loads(res.data)

        self.assertTrue(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test search for a question based on substring
    def test_search_question(self):
        res = self.client().post('/api/questions',
                                 json={'searchTerm': 'soccer'}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)
        self.assertTrue(data['questions'])

    # Test question does not exist
    def test_search_question_error(self):
        res = self.client().post('/api/questions',
                                 json={'searchTerm': 'asdfasdf'}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    # Test get questions based on category
    def test_questions_by_category(self):
        # Pass in Science category
        # Test that the return contains expected number of questions
        current_category = 1
        total_questions = Question.query.filter(Question.category == current_category).all()
        res = self.client().get("/api/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], f"{current_category}")
        self.assertEqual(data['total_questions'], len(total_questions))

    # Test no questions for cateogry tnat does that not exist
    def test_questions_by_category_error(self):
        bad_category = 30
        res = self.client().get(f"/api/categories/{bad_category}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    '''
    DELETE Methods
    '''
    # Test delete question using the first question
    def test_delete_question(self):

        # Post a new question then delete
        payload = {
            "question":
            "Which team won Super Bowl LII?",
            "answer": "Philadelphia Eagles",
            "category": "6",
            "difficulty": 2
        }
        res1 = self.client().post('/api/questions', json=payload)
        question = Question.query.order_by(Question.id.desc()).first()
        question_id = question.id
        res2 = self.client().delete(f'/api/questions/{question_id}')
        data = json.loads(res2.data)

        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    # Test delete question that does not exist returns 422
    def test_delete_questions_error(self):
        res = self.client().delete('/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    '''
    TEST QUIZ
    '''
    # Test quizzes endpoint with science category id and 2 previous questions
    # in Science category returns len of questions -2
    def test_quizzes(self):
        res = self.client().post("/api/quizzes", json={'quiz_category':
                                                       {'id': '1'},
                                                       'previous_questions':
                                                       [20, 22]
                                                       })
        data = json.loads(res.data)
        total_questions = Question.query.filter(Question.category == 1).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(total_questions)-2)
        self.assertTrue(data['question'])

    # Test 0 Total questions if no more questions for category
    def test_quizzes_total_questions(self):
        res = self.client().post("/api/quizzes", json={'quiz_category':
                                                       {'id': '1'},
                                                       'previous_questions':
                                                       [20, 22, 21]
                                                       })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
