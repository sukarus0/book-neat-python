"""
# config.py for DB conn info (db, test_b) and secret key
"""

db = {
    "user": "root",
    "password": "1111",
    "host": "localhost",
    "port": 3306,
    "database": "miniter",
}
DB_URL = (
    f"mysql+mysqlconnector://{db['user']}:"
    + f"{db['password']}@{db['host']}:{db['port']}"
    + f"/{db['database']}?charset=utf8"
)

test_db = {
    "user": "root",
    "password": "1111",
    "host": "localhost",
    "port": 3306,
    "database": "miniter_test",
}
test_config = {
    "DB_URL": f"mysql+mysqlconnector://{test_db['user']}:"
    + f"{test_db['password']}@{test_db['host']}:"
    + f"{test_db['port']}/{test_db['database']}?charset=utf8",
    "JWT_SECRET_KEY": "SOME_SUPER_SECRET_KEY",
}

JWT_SECRET_KEY = "SOME_SUPER_SECRET_KEY"
