"""
---- app.py
"""

from functools import wraps
from flask import Flask, jsonify, request, Response, current_app, g
from flask.json import JSONEncoder
import jwt


class CustomJSONEncoder(JSONEncoder):
    """
    Custom Json Encoder
    """

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def login_required(f):
    """
    login decorate function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is not None:
            try:
                payload = jwt.decode(
                    access_token, current_app.config["JWT_SECRET_KEY"], "HS256"
                )
            except jwt.InvaildTokenError:
                payload = None

            if payload is None:
                return Response(status=401)

            user_id = payload["user_id"]
            g.user_id = user_id
        else:
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated_function


def create_endpoints(app, serivces):
    """
    create endpoints
    """
    app.json_encoder =CustomJSONEncoder

    user_service = services.user_service
    tweet_service = services.tweet_service

    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=["POST"])
    def sign_up():
        new_user = request.json
        new_user = user_service.create_new_user(new_user)

        return jsonify(new_user)

    @app.route("/login", methods=["POST"])
    def login():
        credential = request.json
        authorized = user_service.login(credential)

        if authorized:
            user_credential = user_service.get_user_id_and_password(credential['email'])
            user_id = user_credential['id']
            token = user_service.generate_access_token(user_id)

            return jsonify({"access_token": token, "user_id": user_id})
        else:
            return "", 401

    @app.route("/tweet", methods=["POST"])
    @login_required
    def tweet():
        user_tweet = request.json
        tweet = user_tweet["tweet"]
        user_id = g.user_id

        result = tweet_service.tweet(user_id, tweet)
        if result is None:
            return "exceed 300 chracters", 400

        return "", 200

    @app.route("/follow", methods=["POST"])
    @login_required
    def follow():
        payload = request.json
        user_id = g.user_id
        follow_id = payload['follow']

        user_service.follow(user_id, follow_id)

        return "", 200

    @app.route("/unfollow", methods=["POST"])
    @login_required
    def unfollow():
        payload = request.json
        user_id = g.user_id
        unfollow_id = payload['unfollow']

        user_service.unfollow(user_id, unfollow_id)

        return "", 200

    @app.route("/timeline/<int:user_id>", methods=["GET"])
    def timeline(user_id):
        timeline = tweet_service.get_timeline(user_id)

        return jsonify({"user_id": user_id, "timeline": timeline})

    @app.route("/timeline", methods=["GET"])
    @login_required
    def user_timeline():
        user_id = g.user_id
        timeline = tweet_service.get_timeline(user_id)

        return jsonify({"user_id": user_id, "timeline": timeline})
