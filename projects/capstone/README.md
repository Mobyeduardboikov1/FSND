# Casting Agency - Capstone project for Full Stack Web Developer at Udacity

# URL where the application is hosted: https://castingcapstoneeduard.herokuapp.com/
## Summary
This is the last, capstone project for Full Stack Web Developer. It is divided into frontend and backend.
Frontend is using Auth0 based React boilerplate, and provides a way to communicate with APIs.
Backend is using Flask and SQLAlchemy, and provides CRUD for Actors and Movies, as well as error handling.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

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

## Running the server
To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# Login data
Casting assistant: casting-assistang-eduard@gmail11.com
Casting director: casting-director-eduard@gmail11.com
Executive producer: casting-executive-eduard@gmail11.com

password for all users: @wsX#edC

```
Endpoints
# Actors
GET '/actors'
- Fetches a list of actors with their properties (name, gender, id, age)
- Request Arguments: None
- Returns: An object with success and actors. 
{
  "actors": [
    {
      "age": 55,
      "gender": "Male",
      "id": 1,
      "name": "Bred Pitt"
    }
  ],
  "success": 1
}


POST '/actors'
- Creates an actor
- Request body example
  {
    "name": "Daniel Craig",
    "age": "50",
    "gender": "Male"
  }
- Returns: An object with success, message and id of the actor. 
  {
    "id": 2,
    "message": "Actor has been added",
    "success": 1
  }

PATCH '/actors/<actor_id>'
- Updates an actor
- Request body example
  {
    "name": "Daniel Craig",
    "age": "50",
    "gender": "Male"
  }
- Returns: An object with success, message and id of the actor. 
  {
    "id": 2,
    "message": "Actor has been updated",
    "success": 1
  }

DELETE '/actors/<actor_id>'
- Updates an actor
- Returns: An object with success, message and id of the actor. 
  {
    "id": 2,
    "message": "Actor has been deleted",
    "success": 1
  }

# Movies
GET '/movies'
- Fetches a list of movies with their properties (release_date, title, id)
- Request Arguments: None
- Returns: An object with success and movies. 
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 05 May 1996 00:00:00 GMT",
      "title": "The Rock"
    }
  ],
  "success": 1
}


POST '/movies'
- Creates an actor
- Request body example
  {
    "title": "Die Hard",
    "release_date": "1987-01-01"
  }
- Returns: An object with success, message and id of the movie. 
  {
    "id": 2,
    "message": "Movie has been added",
    "success": 1
  }

PATCH '/movies/<movie_id>'
- Updates a movie
- Request body example
  {
    "title": "Die Hard 3"
  }
- Returns: An object with success, message and id of the movie. 
  {
    "id": 2,
    "message": "Movie has been updated",
    "success": 1
  }

DELETE '/movies/<movie_id>'
- Updates a movie
- Returns: An object with success, message and id of the movie. 
  {
    "id": 2,
    "message": "Movie has been deleted",
    "success": 1
  }

Present error handlers: 404, 422, 400, 405 and 500
```


## Testing
To run the tests, run
- NOTE: Test db was not used
```
python test_app.py
```