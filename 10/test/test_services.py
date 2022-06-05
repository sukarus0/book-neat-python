"""
---- test_services.py
"""

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import jwt
import bcrypt
import pytest
import config

from model import UserDao, TweetDao
from service import UserService, TweetService
from sqlalchemy import create_engine, text

database = create_engine(
        config.test_config['DB_URL'],
        encoding='utf-8',
        max_overflow=0)

@pytest.fixture
def user_service():
    return UserService(UserDao(database), config.test_config)

@pytest.fixture
def tweet_service():
    return TweetService(TweetDao(database))

def setup_function():
    hashed_password = bcrypt.hashpw(
            b"1111",
            bcrypt.gensalt()
        )
    new_users = [
            {
                'id' : 1,
                'name' : 'dwlee',
                'email' : 'dwlee@gmail.com',
                'profile' : 'professor',
                'hashed_password' : hashed_password
            }, {
                'id' : 2,
                'name' : 'jmhan',
                'email' : 'jmhan@gmail.com',
                'profile' : 'actress',
                'hashed_password' : hashed_password
            }
        ]

    database.execute(text(
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
        ), new_users)
    
    database.execute(text(
        """
            INSERT INTO tweets (
                user_id,
                tweet
            ) VALUES (
                2,
                "I love him."
            )
        """
        ))


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def get_user(user_id):
    """
    user get function
    """
    user = database.execute(
        text(
            """
        SELECT
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """
        ),
        {"user_id": user_id},
    ).fetchone()

    return (
        {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "profile": user["profile"],
        }
        if user
        else None
    )


def get_follow_list(user_id):
    rows = database.execute(text(
        """
            SELECT follow_user_id as id
            FROM users_follow_list
            WHERE user_id = :user_id
        """
        ), {
            'user_id' : user_id
        }
    ).fetchall()

    return [int(row['id']) for row in rows]


def test_create_new_user(user_service):
    new_user = {
            'name' : 'hjseo',
            'email' : 'hjseo@gmail.com',
            'profile' : 'actress',
            'password' : '2222'
        }

    new_user_id = user_service.create_new_user(new_user)
    user = get_user(new_user_id)

    assert user == {
            'id'    : new_user_id,
            'name'  : new_user['name'],
            'email' : new_user['email'],
            'profile' : new_user['profile']
        }


def test_generate_access_token(user_service):
    token = user_service.generate_access_token(1)
    payload = jwt.decode(token, config.JWT_SECRET_KEY, 'HS256')

    assert payload['user_id'] == 1


def test_follow(user_service):
    user_service.follow(1, 2)

    follow_list = get_follow_list(1)

    assert follow_list == [2]


def test_unfollow(user_service):
    user_service.follow(1, 2)
    user_service.unfollow(1, 2)

    follow_list = get_follow_list(1)

    assert follow_list == []


def test_tweet(tweet_service):
    tweet_service.tweet(1, "tweet test")
    timeline = tweet_service.timeline(1)

    assert timeline == [
        {
            'user_id' : 1,
            'tweet' : 'tweet test'
        }
    ]


def test_timeline(user_service, tweet_service):
    tweet_service.tweet(1, "tweet test")
    tweet_service.tweet(2, "tweet test 2")
    user_service.follow(1, 2)

    timeline = tweet_service.timeline(1)

    assert timeline == [
        {
            'user_id' : 2,
            'tweet' : 'I love him.'
        },
        {
            'user_id' : 1,
            'tweet' : 'tweet test'
        },
        {
            'user_id' : 2,
            'tweet' : 'tweet test 2'
        }
    ]
