import json
import os
import unittest

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from app import app
from database.models import Actor, Movie, setup_db
from test_data import (edited_actor_info, edited_movie_info, new_actor_info,
                       new_movie_info)

load_dotenv('.env')
database_path = os.getenv('DATABASE_TEST_URL')
assistant_token = os.getenv('ASSISTANT_TEST_TOKEN')
director_token = os.getenv('DIRECTOR_TEST_TOKEN')
producer_token = os.getenv('PRODUCER_TEST_TOKEN')


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app, database_path)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def set_headers(self, token=None):
        if token is None:
            return {}
        else:
            return {
                'Authorization': 'Bearer ' + token
            }

# GET-methods

    def test_get_movies(self, token=assistant_token):
        response = self.client().get('/movies', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_without_auth(self):
        response = self.client().get('/movies')
        self.assertEqual(response.status_code, 401)

    def test_get_actors(self, token=assistant_token):
        response = self.client().get('/actors', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_without_auth(self):
        response = self.client().get('/actors')
        self.assertEqual(response.status_code, 401)

# POST-methods

    def test_try_to_create_actor_without_auth(self):
        info = new_actor_info
        response = self.client().post('/actors', json=info)

        self.assertEqual(response.status_code, 401)

    def test_try_to_create_actor_without_permission(self, token=assistant_token):
        info = new_actor_info
        response = self.client().post('/actors', json=info, headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Access denied')

    def test_try_to_create_actor_with_empty_values(self, token=director_token):
        info = {'name': ''}
        response = self.client().post('/actors', json=info, headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_create_actor(self, token=director_token):
        info = new_actor_info
        response = self.client().post('/actors', json=info, headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(info['id'], data['actor']['id'])
        self.assertEqual(info['name'], data['actor']['name'])
        self.assertEqual(info['gender'], data['actor']['gender'])

    def test_try_to_create_movie_without_auth(self):
        info = new_movie_info
        response = self.client().post('/movies', json=info)
        self.assertEqual(response.status_code, 401)

    def test_try_to_create_movie_without_permission(self, token=assistant_token):
        info = new_movie_info
        response = self.client().post('/movies', json=info, headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Access denied')

    def test_try_to_create_movie_with_empty_values(self, token=producer_token):
        info = {'title': ''}
        response = self.client().post('/movies', json=info, headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_create_movie(self, token=producer_token):
        info = new_movie_info
        response = self.client().post('/movies', json=info, headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(info, data['movie'])


# PATCH-methods


    def test_try_to_edit_actor_without_auth(self):
        info = edited_actor_info
        response = self.client().patch('/actors/3', json=info)
        self.assertEqual(response.status_code, 401)

    def test_try_to_edit_actor_without_permission(self, token=assistant_token):
        info = edited_actor_info
        response = self.client().patch('/actors/3', json=info,
                                       headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Access denied')

    def test_edit_actor(self, token=director_token):
        info = edited_actor_info
        response = self.client().patch('/actors/3', json=info,
                                       headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(info['name'], data['actor']['name'])
        self.assertEqual(info['movie_id'], data['actor']['movie_id'])

    def test_try_to_edit_movie_without_auth(self):
        info = edited_movie_info
        response = self.client().patch('/movies/3', json=info)
        self.assertEqual(response.status_code, 401)

    def test_try_to_edit_movie_without_permission(self, token=assistant_token):
        info = edited_movie_info
        response = self.client().patch('/movies/3', json=info,
                                       headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Access denied')

    def test_edit_movie(self, token=director_token):
        info = edited_movie_info
        response = self.client().patch('/movies/3', json=info,
                                       headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(info['title'], data['movie']['title'])


# DELETE-methods


    def test_try_to_delete_actor_without_auth(self):
        response = self.client().delete('/actors/10')

        self.assertEqual(response.status_code, 401)

    def test_try_to_delete_nonexistent_actor(self, token=director_token):
        response = self.client().delete('/actors/100', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_try_to_delete_actor_without_permission(self, token=assistant_token):
        response = self.client().delete('/actors/100', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Access denied')

    def test_delete_actor(self, token=director_token):
        response = self.client().delete('/actors/10', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['deleted']))

    def test_try_to_delete_movie_without_auth(self):
        response = self.client().delete('/movies/10')

        self.assertEqual(response.status_code, 401)

    def test_try_to_delete_nonexistent_movie(self, token=producer_token):
        response = self.client().delete('/movies/100', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_try_to_delete_movie_without_permission(self, token=director_token):
        response = self.client().delete('/movies/100', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['message'], 'Access denied')

    def test_delete_movie(self, token=producer_token):
        response = self.client().delete('/movies/10', headers=self.set_headers(token))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['deleted']))


if __name__ == '__main__':
    unittest.main()
