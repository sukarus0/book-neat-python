"""
---- Tweet App Test
"""

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import json
import pytest
import bcrypt
from sqlalchemy import create_engine, text

import config
from app import create_app

database = create_engine(config.test_config["DB_URL"], encoding="utf-8", max_overflow=0)


@pytest.fixture
def api():
    """
    pytest.fixture to substitute real API app.
    """
    app = create_app(config.test_config)
    app.config["TEST"] = True
    api = app.test_client()

    return api


def setup_function():
    """
    setup for every test
    """
    hashed_password = bcrypt.hashpw(b"1111", bcrypt.gensalt())
    new_user = {
        "id": 1,
        "name": "TaeYeon",
        "email": "taeyeon@gmail.com",
        "profile": "singer",
        "hashed_password": hashed_password,
    }
    database.execute(
        text(
            """
        INSERT INTO users (
            id,
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :id,
            :name,
            :email,
            :profile,
            :hashed_password
        )
    """
        ),
        new_user,
    )


def teardown_function():
    """
    teardown for every test
    """
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_ping(api):
    """
    ping test
    """
    resp = api.get("/ping")
    assert b"pong" in resp.data


def test_sign_up(api):
    """
    sign up test
    """
    # create test user
    new_user = {
        "email": "kim@gmail.com",
        "password": "1111",
        "name": "jkkim",
        "profile": "model",
    }

    resp = api.post(
        "/sign-up", data=json.dumps(new_user), content_type="application/json"
    )

    assert resp.status_code == 200


def test_login(api):
    """
    login test
    """
    # login
    resp = api.post(
        "/login",
        data=json.dumps({"email": "taeyeon@gmail.com", "password": "1111"}),
        content_type="application/json",
    )

    assert resp.status_code == 200


def test_tweet(api):
    """
    tweet test
    """
    resp = api.post(
        "/login",
        data=json.dumps({"email": "taeyeon@gmail.com", "password": "1111"}),
        content_type="application/json",
    )

    resp_json = json.loads(resp.data.decode("utf-8"))
    access_token = resp_json["access_token"]
    new_user_id = resp_json["user_id"]

    resp = api.post(
        "tweet",
        data=json.dumps({"tweet": "Please fuck me"}),
        content_type="application/json",
        headers={"Authorization": access_token},
    )
    assert resp.status_code == 200

    # check tweet
    resp = api.get(f"/timeline/{new_user_id}")
    tweets = json.loads(resp.data)

    assert resp.status_code == 200
    assert tweets == {
        "user_id": 1,
        "timeline": [{"user_id": 1, "tweet": "Please fuck me"}],
    }
