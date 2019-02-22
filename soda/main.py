from uuid import uuid4
import os
import hashlib, hmac
import logging

import socketio
from sanic.views import HTTPMethodView
from sanic.response import json as json_response
from sanic import Sanic
from sanic_jwt import Initialize as setupJWT, exceptions
from sanic_cors import CORS, cross_origin

from aiocassandra import aiosession
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.connection import register_connection, \
    set_default_connection

from .models.user import User
from .models.project import Project
from .models.record import Record

from .routes import setup_routes
from .settings import SETTINGS

logger = logging.getLogger(__name__)


async def authenticate(request, *args, **kwargs):
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        raise exceptions.AuthenticationFailed("Missing email or password.")

    user = User.objects().filter(email=email).allow_filtering().first()
    if not user:
        raise exceptions.AuthenticationFailed("User not found.")

    login_pass = hashlib.sha256(password.encode()).hexdigest()

    passwords_matches = hmac.compare_digest(user.password, login_pass)
    if not passwords_matches:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    print(type(user.id))
    user = dict(user)
    user['user_id'] = str(user['id'])
    return user


async def scope_extender(user, *args, **kwargs):
    return user['scopes']


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user = User.objects(id=payload['user_id']).first()
        user['id'] = str(user['id'])
        return dict(user)
    else:
        return None

async def setup_cassandra(app, loop):
    logger.warning('Initializing Database')

    cluster = Cluster(['cassandra_seed_node'])
    session = cluster.connect()
    session.execute(
        """CREATE KEYSPACE IF NOT EXISTS soda WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;""")
    session.execute('USE soda')

    register_connection(str(session), session=session)
    set_default_connection(str(session))
    sync_table(User, keyspaces=['soda'])
    sync_table(Record, keyspaces=['soda'])
    sync_table(Project, keyspaces=['soda'])

    aiosession(session)
    app.db = session
    return app


def create_app(settings=SETTINGS):
    sio = socketio.AsyncServer()

    app = Sanic()

    app.config.update(settings)
    app = setup_routes(app)


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80, debug=True)
