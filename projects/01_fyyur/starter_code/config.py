import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = 'postgres://eduardnix:2wsx3edc@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_SECRET_KEY = '123asdasd9873kjhfksdyf98349df'

