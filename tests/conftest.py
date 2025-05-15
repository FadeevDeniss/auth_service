import binascii
import os
import uuid

import jwt
import pytest
import redis

from datetime import datetime, timedelta

from django.conf import settings

from api.crypto_utils import sign_jwt
from api.models import UserProfile
from api.views.auth import RegistrationView, LoginView, RefreshTokenView


@pytest.fixture
def redis_client():

    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )

    yield client

    client.flushdb(asynchronous=False)
    records_after = len(client.scan()[1])
    assert records_after == 0, \
        f"Redis has not been flushed correctly. Finished with size: {records_after}"


# =============== Views fixtures ==============


@pytest.fixture(scope='class')
def registration_view():
    return RegistrationView.as_view()


@pytest.fixture(scope='class')
def login_view():
    return LoginView.as_view()


@pytest.fixture(scope='class')
def refresh_token_view():
    return RefreshTokenView.as_view()


@pytest.fixture
def created_user(django_db_setup, django_db_blocker, valid_credentials):
    with django_db_blocker.unblock():
        return UserProfile.objects.create_user(
            username='test_user_01', **valid_credentials)


@pytest.fixture
def redis_add_document(redis_client):
    redis_client.set(str(uuid.uuid4()), 0)


@pytest.fixture
def jwt_id():
    return str(uuid.uuid4())


@pytest.fixture
def jwt_payload(created_user, jwt_id):
    now = datetime.now()
    delta = timedelta(seconds=settings.REFRESH_TOKEN_EXP)

    return {
        'id': created_user.pk,
        'iat': round(int(now.timestamp())),
        'exp': round(int((now + delta).timestamp()))
    }


@pytest.fixture
def token(jwt_payload, jwt_id):
    jwt_payload['jti'] = jwt_id

    return jwt.encode(
        jwt_payload,
        settings.ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )


@pytest.fixture
def refresh_token(jwt_payload):
    return jwt.encode(
        jwt_payload,
        settings.REFRESH_TOKEN_SECRET,
        algorithm='HS256'
    )


@pytest.fixture
def expired_refresh_token(created_user, jwt_payload):
    jwt_payload['exp'] = round(int(datetime.now().timestamp()))
    return sign_jwt(created_user.pk, settings.REFRESH_TOKEN_SECRET, 0)


@pytest.fixture
def invalid_refresh_token(jwt_payload):
    secret = binascii.hexlify(os.urandom(24))
    return jwt.encode(
        jwt_payload,
        secret,
        algorithm='HS256'
    )


@pytest.fixture
def refresh_token_invalid_pk(jwt_payload):
    jwt_payload['id'] = 5
    return jwt.encode(
        jwt_payload,
        settings.REFRESH_TOKEN_SECRET,
        algorithm='HS256'
    )


@pytest.fixture(scope='session')
def valid_credentials():
    return {'email': 'testmail@dev.com', 'password': 'secret12345!'}

