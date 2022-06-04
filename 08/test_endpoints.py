import config

from sqlalchemy import create_engine, text

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)

import pytest
from app import create_app
import json

new_user_id = 0

@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api;


def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_sign_up(api):
    # create test user
    new_user = {
            'email'     : 'kim@gmail.com',
            'password'  : '1111',
            'name'      : 'jkkim',
            'profile'   : 'model'
    }

    resp = api.post(
            '/sign-up',
            data = json.dumps(new_user),
            content_type = 'application/json'
    )

    assert resp.status_code == 200

    resp_json = json.loads(resp.data.decode('utf-8'))
    new_user_id = resp_json['id']


def test_login(api):
    # login
    resp = api.post(
            '/login',
            data = json.dumps({'email':'kim@gmail.com', 'password':'1111'}),
            content_type = 'application/json'
    )

    assert resp.status_code == 200


def test_tweet(api):

    resp = api.post(
            '/login',
            data = json.dumps({'email':'kim@gmail.com', 'password':'1111'}),
            content_type = 'application/json'
    )

    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']
    new_user_id = resp_json['user_id']

    resp = api.post(
            'tweet',
            data = json.dumps({'tweet': 'Please fuck me'}),
            content_type = 'application/json',
            headers = {'Authorization' : access_token}
    )
    assert resp.status_code == 200

    # check tweet
    resp = api.get(f'/timeline/{new_user_id}')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
                'user_id' : 1,
                'timeline' : [
                    {
                        'user_id' : 1,
                        'tweet' : 'Please fuck me'
                    }
                ]
            }
