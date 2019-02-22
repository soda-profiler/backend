import pytest, os
from sanic import Sanic, response
from soda.main import create_app
import hashlib
from asynctest import patch as asyncpatch

TEST_SETTINGS = dict(
    DB_NAME="test",
    DB_USER="test",
    DB_PASSWORD=None,
    DB_HOST="",
    DB_PORT=os.getenv("DATABASE_PORT"),
    DRIVER_NAME="postgres",
    JWT_SECRET='Zp93aeJYrZtdpAb7kHh32fxoGpV6FRfy',
    JWT_ALGORITHM='HS256',
    JWT_EXP_DELTA_SECONDS=259200,
    TEST=True,
)


@pytest.yield_fixture
def app():
    app = create_app(TEST_SETTINGS)
    yield app


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app))


#########
# Tests #
#########

async def test_client_create_user_with_valid_credentials(test_cli):
    """
    POST request
    """
    resp = await test_cli.post('/api/v1.0/users', json={
        "email": "test@test.com",
        "password": "test"
    })
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {
        "email": "test@test.com",
        "password": hashlib.sha256(b"test").hexdigest()
    }


async def test_client_signup_without_password_field(test_cli):
    """
    POST request
    """
    resp = await test_cli.post('/api/v1.0/users', json={
        "email": "test@test.com",
    })
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {}


async def test_get_without_filter_limits_100(test_cli):
    """
    POST request
    """
    with asyncpatch('soda.views.user.User') as UserModel:
        UserModel.return_value = []
        resp = await test_cli.post(
            '/api/v1.0/users',
            json={
                "email": "test@test.com",
            })

        resp_json = await resp.json()
    assert resp_json == []
