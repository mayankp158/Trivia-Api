import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
categorysi = {"Science": 1,
    "Art":2,
    "Geography":3,
    "History":4,
    "Entertainment":5,
    "Sports":6
}



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)





  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  def paginate_ques(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_ques = questions[start:end]
    return current_ques

  def getErrorMessage(error, default_text):
    try:

      return error.description["message"]
    except TypeError:

      return default_text

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def retrieve_category():
    categories = Category.query.all()
    all_category = [category.format() for category in categories]
    returned_categories = []
    for cat in all_category:
      returned_categories.append(cat['type'])
    return jsonify({
      'success': True,
      'total_categories': returned_categories,
      'number_of_categories': len(returned_categories)

    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    paginate_questions = paginate_ques(request, selection)
    if len(paginate_questions) == 0:
      abort(404)
    categories = Category.query.all()
    all_category = [category.format() for category in categories]
    returned_categories = []
    for cat in all_category:
      returned_categories.append(cat['type'])

    return jsonify({
      'success': True,
      'questions': paginate_questions,
      'total_questions': len(selection),
      'categories': returned_categories,
      'current_category': len(returned_categories)
    })






  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID.
   
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404, {'message': 'Question with id {} does not exist.'.format(question_id)})
      try:
        question.delete()
        selection = Question.query.order_by(Question.id).all()
        current_question = paginate_ques(request, selection)
        return jsonify ({
            'success': True,
            'deleted': question_id,
            'questions': current_question,
            'total_questions': len(Question.query.all())
          })
      except:
        abort(422)

  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    new_question = body.get('question',None)
    new_category = body.get('category',None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty',None)
    if not new_question:

      abort(400, {'message': 'Question can not be blank'})


    if not new_answer:

      abort(400, {'message': 'Answer can not be blank'})

    if not new_category:

      abort(400, {'message': 'Category can not be blank'})

    if not new_difficulty:

      abort(400, {'message': 'Difficulty can not be blank'})
    try:
        user_question = Question(question=new_question, answer=new_answer,category=new_category,difficulty=new_difficulty)
        user_question.insert()
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_ques(request, selection)
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]
        return jsonify ({
          'success': True,
          'created': user_question.id,
          'questions': current_questions ,
          'total_questions': len(Question.query.all()),
          'current_category': categories_all
        })
    except:
      abort(422)






  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/question', methods=['POST'])
  def search_ques():
    body = request.get_json()
    print(body)

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    searching_term = body.get('searchTerm', None)
    if searching_term:
      #question_searched = Question.query.filter(Question.question).all()
      #if any(searching_term in s for s in question_searched):

      question_searched = Question.query.filter(Question.question.contains(searching_term)).all()
      print(question_searched)
      if not question_searched:
        abort(404, {'message': 'no questions that contains "{}" found.'.format(searching_term)})
      questions_found = [question.format() for question in question_searched]
      selections = Question.query.order_by(Question.id).all()
      categories = Category.query.all()
      all_category = [category.format() for category in categories]
      return jsonify ({
        'success': True,
        'questions': questions_found,
        'total_questions': len(selections),
        'current_category': all_category
      })

    # new_question = body.get('question', None)
    # new_category = body.get('category', None)
    # new_answer = body.get('answer', None)
    # new_difficulty = body.get('difficulty', None)
    # if not new_question:
    #   abort(400, {'message': 'Question can not be blank'})
    #
    # if not new_answer:
    #   abort(400, {'message': 'Answer can not be blank'})
    #
    # if not new_category:
    #   abort(400, {'message': 'Category can not be blank'})
    #
    # if not new_difficulty:
    #   abort(400, {'message': 'Difficulty can not be blank'})
    #
    # try:
    #     user_question = Question(question=new_question, answer=new_answer,category=new_category,difficulty=new_difficulty)
    #     user_question.insert()
    #     selection = Question.query.order_by(Question.id).all()
    #     current_questions = paginate_ques(request, selection)
    #
    #     return jsonify ({
    #       'success': True,
    #       'created': user_question.id,
    #       'questions': current_questions,
    #       'total_questions': len(Question.query.all())
    #     })
    # except:
    #   abort(422)



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/questions/category/<int:category_id>', methods=['GET'])
  def category_int_request(category_id):
    categories = Question.query.filter(Question.category == category_id).all()
    #ques_found = categories.order_by(Question.id).all()
    category_found = [category.format() for category in categories]
    print(category_found)

    return jsonify({
      'success': True,
      'current_category': category_found
    })

  @app.route('/categories/<string:category_id>/questions', methods=['GET'])
  def category_string_req(category_id):

    matched = (Question.query.filter(Question.category == int(category_id)+1).order_by(Question.id).all())
    print(matched)
    category_found = [category.format() for category in matched]
    print(category_found)
    return jsonify ({
      'success': True,
      'current_category': category_found,
      'total_question':category_found,
      'questions':category_found
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    if not body:
      abort(400, {'message': 'Please provide a JSON body with previous question Ids and optional category.'})
    previous_ques = body.get('previous_ques',None)
    category_selected = body.get('quiz_category',None)
    print(category_selected)


    if not previous_ques:
      if category_selected['id']!=10:
        ques_given = (Question.query.filter(Question.category == str(int(category_selected['id'])+1)).all())

      else:
        ques_given = (Question.query.all())

    else:
      if category_selected['id']!=10:
        ques_given = (Question.query.filter(Question.category == str(int(category_selected['id'])+1)).filter(Question.id.notin_(previous_ques)).all())
      else:
        ques_given = (Question.question.filter(Question.id.notin_(previous_ques)).all())

    ques_formatted = [question.format() for question in ques_given]

    random_ques =  random.choice(ques_formatted)

    return jsonify ({
      'success': True,
      'question': random_ques
    })



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message":  getErrorMessage(error, "bad request")
    }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": getErrorMessage(error, "resource not found")
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": getErrorMessage(error, "unprocessable")
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500
  
  return app

    