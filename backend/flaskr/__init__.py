import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    format_questions = [q.format() for q in selection]
    current_questions = format_questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)

    '''
    Done: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    Done: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('ACCESS-CONTROL-ALLOW-HEADERS',
                             'Content-Type,Authorization,true')
        response.headers.add('ACCESS-CONTROL-ALLOW-METHODS',
                             'POST,GET,PATCH,DELETE,PUT')
        return response
    '''
    Done:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    def categories_list():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        return categories

    @app.route('/api/categories')
    def all_categories():

        categories = categories_list()
        return jsonify({
          'success': True,
          'categories': categories,
          'total_categories': len(categories)
        })

    @app.route('/api/categories/<category_id>')
    def category_by_id(category_id):
        category = Category.query.get(category_id)
        formatted_category = category.format()
        return jsonify({
          'success': True,
          'category': formatted_category
        })
    '''
    Done:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at
    the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/api/questions')
    def all_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection),
          'current_category': None,
          'categories': categories_list(),
        })

    '''
    Done:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/api/questions/<question_id>', methods=['DELETE'])
    def question_by_id(question_id):
        try:
            question = Question.query.filter(
                                             Question.id == question_id
                                             ).one_or_none()

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
              'success': True,
              'deleted': question.id,
              'questions': current_questions,
            })
        except:
            abort(422)

    '''
    Done:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.

    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/api/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)

        try:
            if search_term:
                searched_questions = Question.query.filter(
                                                          Question.question.ilike(
                                                            f"%{search_term}%")
                                                          ).all()
                p_questions = paginate_questions(request, searched_questions)

                return jsonify({
                  'success': True,
                  'questions': p_questions,
                  'total_questions': len(p_questions),
                  'current_category': None
                })

            else:
                if new_question == '' or new_answer == '':
                    abort(422)

                new_question = Question(question=new_question,
                                        answer=new_answer,
                                        category=new_category,
                                        difficulty=new_difficulty
                                        )
                new_question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)
                posted_question = Question.query.filter(
                                                        Question.answer == new_question.answer
                                                        ).one_or_none()

                return jsonify({
                  'success': True,
                  'question_id': posted_question.id,
                  'questions': current_questions,
                  'total_questions': len(selection)
                })

        except:
            abort(422)

    '''
    Done:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/api/categories/<category_id>/questions')
    def questions_by_category(category_id):
        # get questions with category id == to category_id
        try:
            questions = Question.query.filter(
                                              Question.category == category_id
                                              ).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': len(current_questions),
              'current_category': category_id
              })
        except:
            abort(404)

    '''
    Done:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    # Get a question based on a category, or all categories
    # return a random question from that category
    # if not in previous questions
    @app.route('/api/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        previous_question = body.get('previous_questions', None)
        category = body.get('quiz_category')
        current_category = category.get('id')

        if current_category != 0:
            current_questions = Question.query.filter(
                                                      Question.category == current_category
                                                      ).all()
        else:
            current_questions = Question.query.all()

        questions = []
        for q in current_questions:
            if q.id not in previous_question:
                questions.append(q)

        if len(questions) == 0:
            return jsonify({
              'success': True
            })

        random_question = random.choice(questions)
        format_question = random_question.format()
        # return random question
        return jsonify({
          'success': True,
          'question': format_question,
          'total_questions': len(questions),
        })
    '''
    Done:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource Not Found',
        }), 404

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable Request'
        }), 422

    @app.errorhandler(500)
    def unprocessable_request(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
        }), 500

    return app
