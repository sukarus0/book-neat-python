"""
---- test_model.py
"""

import bcrypt
import pytest
import config

from model import UserDao, TweetDao
from sqlalchemy import create_engine, text

database = create_engine(
        config.test_config['DB_URL'],
        encoding='utf-8',
        max_overflow=0)

@pytest.fixture
def user_dao():
    return UserDao(database)

def setup_function():
    hashed_password = brcypt.hashpw(
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

def test_insert_user(user_dao):
    new_user = {
            'name' : 'hjseo',
            'email' : 'hjseo@gmail.com',
            'profile' : 'actress',
            'hashed_password' : '2222'
        }

    new_user_id = user_dao.insert_user(new_user)
    user = get_user(new_user_id)

    assert user == {
            'id'    : new_user_id,
            'name'  : new_user['name'],
            'email' : new_user['email'],
            'profile' : new_user['profile']
        }
