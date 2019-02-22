import asyncio
from uuid import uuid4
import hashlib
import hmac
from datetime import datetime
import functools

from sanic.views import HTTPMethodView
from sanic.request import Request
import sanic.response as res
from sanic_jwt.decorators import protected
from cassandra.cqlengine.query import LWTException

from ..models.user import User


class UserView(HTTPMethodView):
    decorators = []

    async def get(self, request: Request):
        """
        Retrieve the (limit) most recently created users.
        :param request: Request
        :return: list
        """
        n_users = request.json.get('limit', 100)

        users = User.objects.all().order_by('created_at').limit(n_users)

        # cast uuid to str
        payload = [
            {**user, "id": str(user['id'])}
            for user in users
        ]

        return res.json(payload)


    async def post(self, request: Request):
        payload = request.json
        if not payload or 'email' not in payload or 'password' not in payload:
            return res.json({
                "exception": "Bad Request",
                "reasons": "email and password is required"
            }, status=400)

        payload['password'] = hashlib.sha256(
            payload['password'].encode()).hexdigest()
        payload['scopes'] = ["user", ]

        user_exists = User.objects(
            email=payload['email']).allow_filtering().first()
        if user_exists:
            return res.json({
                "message": "User Already Exists",
            }, status=409)

        try:
            user = User.create(**payload).if_not_exists()
        except LWTException as lwt:
            return res.json({
                "status": 201,
                "message": "User Already Exists",
                "user_id": str(lwt.existing['id'])
            })
        return res.json({
            "status": 201,
            "message": "User Created",
            "user_id": str(user.id)
        })
