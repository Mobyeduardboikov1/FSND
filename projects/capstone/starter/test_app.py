import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import *

TOKENS = {
    'casting_executive_producer': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVTdjBncXRYS2lpeU5SZ1Q1aUlyRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03cDd6Zm1nay5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjNjIwYjk0NDg5NGEwMDY4MDgwMmExIiwiYXVkIjpbImh0dHA6Ly8iLCJodHRwczovL2Rldi03cDd6Zm1nay5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA3OTU2NjQxLCJleHAiOjE2MTA1NDg2NDEsImF6cCI6IlAwS3FMWEJ0MVNFOVpURzI5RGtSbVZCS2N1V3ZQeTJ3Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.J53AUBjXSFu0TO0HM_xkhGB5fIbmhtMHUjncP4vG5pknmT7hioN6jkJtGAQMPNOxc9UWz6HmYxrRYulsD_stYI73e1uXL_vllkN4TQbWUwsi7QdHOypEz-V5HwccCDraiAEBHvrP1R2zuVhHrTXITvUuY1_4Kg9z4qT4e_dVuWo22kXFFyirh3NHqG6b-bIpX2GBvUF1cI-AvN3jcHWKnB8zRXPgqZEGUDOgzuPXk6wb7cyAT4lGR-I2J8oyYlD27VG6k4D-f8IDeFLMdKDO3dJt1mTArR0e3hMoAJIKEOg1gxl4kFweNYNXCTSA7KaLeT7-0cXYkt1EtvUve1BmOA'
}

class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting"
        self.database_path = "postgres://{}/{}".format('eduardnix:2wsx3edc@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        # Delete any test records
        delete_q = Movie.__table__.delete().where(Movie.title == 'Test movie')
        db.session.execute(delete_q)
        db.session.commit()

        delete_q = Actor.__table__.delete().where(Actor.name == 'Test actor')
        db.session.execute(delete_q)
        db.session.commit()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """ Get actors """
    def test_01_get_actors(self):
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)
        actor_count = Actor.query.count()
        self.assertEqual(data['success'], 1)
        self.assertEqual(len(data['actors']), actor_count)
    
    """ Get movies """
    def test_02_get_movies(self):
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)
        movie_count = Movie.query.count()
        self.assertEqual(data['success'], 1)
        self.assertEqual(len(data['movies']), movie_count)
    
    
    """ Add new actor """
    def test_03_new_actor(self):
        new_actor = Actor(
            name='Test actor',
            age=10,
            gender='male'
        )
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        res = self.client().post('/actors', json=new_actor.format(), headers=headers)
        data = json.loads(res.data)


        inserted_actor = Actor.query.filter_by(name='Test actor').one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(inserted_actor.name, 'Test actor')
    
    """ Fail adding new actor because of wrong request type """
    def test_04_new_actor_fail(self):
        new_actor = Actor(
            name='Test actor',
            age=10,
            gender='male'
        )
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        res = self.client().patch('/actors', json=new_actor.format(), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method not allowed')
    
    """ Add new movie """
    def test_05_new_movie(self):
        new_movie = Movie(
            title='Test movie',
            release_date='1990-01-01'
        )
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        res = self.client().post('/movies', json=new_movie.format(), headers=headers)
        data = json.loads(res.data)

        inserted_movie = Movie.query.filter_by(title='Test movie').one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(inserted_movie.title, 'Test movie')
    
    """ Fail adding new movie because of wrong request type"""
    def test_06_new_movie_fail(self):
        new_movie = Movie(
            title='Test movie',
            release_date=None
        )
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        res = self.client().patch('/movies', json=new_movie.format(), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method not allowed')
   
    
    """ Delete a movie """
    def test_07_delete_movie(self):
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }
        movie = Movie.query.filter_by(title='Test movie').one_or_none()
        if (movie is None):
            movie = Movie(
            title='Test movie',
            release_date='1900-01-01'
            )
            movie.insert()

        res = self.client().delete('/movies/' + str(movie.id), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Movie has been deleted')

    """ Delete an actor """
    def test_08_delete_actor(self):
        headers = {
            "Authorization": TOKENS["casting_executive_producer"]
        }     
        actor = Actor.query.filter_by(name='Test actor').one_or_none()
        if (actor is None):
            actor = Actor(
                name='Test actor',
                age=30,
                gender='male'
            )
            actor.insert()
        res = self.client().delete('/actors/' + str(actor.id), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Actor has been deleted')
    
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()