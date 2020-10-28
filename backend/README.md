# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
### Testing
To run tests using the test database file provided, with Postgres running, enter the commands:

```bash
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Getting Started

BASE URL: The backend is hosted at the default URL, http://127.0.0.1:5000

### Endpoints

#### GET /api/categories
* Fetches a dictionary of categories in which the key matches id and value matches the of the string corresponding to the respective category.
* Returns an object, categories, that contains objects of id:category string key:value pairs along with the total number of categories.
```
{
  '1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"
}
```

#### GET /api/categories/<category_id>

* Fetches a dictionary object of the category matching the category id specified in the URI
* Returns: single object of id:category string key:value pair.
```
{
    "category":{
        "id":1,
        "type":"Science"
        },
        "success":true
}
```

#### GET /api/questions

* Fetches a dictionary of paginated questions containing the keys: id, question, answer, category, and difficulty along with their values.
* Returns: an object with key, questions, containing objects of id:id, question: question string, answer: answer string, category: category int, and difficulty: difficulty int; the total amount of questions in the database, and the an object, categories, of id:category string key:value pair.

```
{
    "categories":{
        "1":"Science",
        "2":"Art","3":"Geography",
        ...
        },
        "current_category":null,
        "questions":[{
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },{
                "answer":"Maya Angelou",
                "category":4,
                "difficulty":2,
                "id":5,
                "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },...],
        "success":true,
        "total_questions":18
        }
}
```

#### POST /api/questions

1) Creates a question by sending a post method to the database
  - Request arguments: JSON dictionary object of keys: value pairs question: question string, answer: answer string, category: category int, and difficulty: difficulty int and their respective values

  '''

  '''
  - Returns: an object with key, questions, containing objects of id:id, question: question string, answer: answer string, category: category int, and difficulty: difficulty int; the total amount of questions in the database


  
OR

2) Search for questions using a substring.
  - Request arguments: dictionary object of key:value searchTerm:substring.
  - Returns: an object containing objects for questions, and total questions.



#### DELETE /api/questions/<question_id>

* Deletes a question from the database
* Request arguments: None
* Returns: An object of the deleted question's id and all questions paginated.

#### GET /api/categories/<category_id>/questions

* Fetches all of the questions contained in category matching the category_id
* Returns: An object, questions, containing an object for each question with a category id matching category_id; an object of total_questions related to the specified category; an object of key:value pair current category: category.id

```
{
  "current_category": "1", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```
#### POST /api/quizzes

* 
* Request arguments: previous question and current category

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
