import uuid

from datetime import timedelta, datetime

import jwt
from jwt import encode
from django.conf import settings
from rest_framework import exceptions

from api.models import UserProfile


def generate_jwt_keypair(user_id: int):
    """
    Generates keypair of access_token and refresh_token
    """
    access_token_expires = timedelta(seconds=int(settings.ACCESS_TOKEN_LIFETIME))
    refresh_token_expires = timedelta(seconds=int(settings.REFRESH_TOKEN_LIFETIME))

    access_token = encode(
        {
            'id': user_id,
            'iat': int(datetime.now().timestamp()),
            'exp': int((datetime.now() + access_token_expires).timestamp()),
        },
        settings.ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )
    refresh_token = encode(
        {
            'id': user_id,
            'jti': str(uuid.uuid4()),
            'iat': int(datetime.now().timestamp()),
            'exp': int((datetime.now() + refresh_token_expires).timestamp())
        },
        settings.REFRESH_TOKEN_SECRET,
        algorithm='HS256'
    )
    return access_token, refresh_token


def verify_jwt_token(token: str, secret: str):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token expired.')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token')

    try:
        return UserProfile.objects.get(id=payload['id']), payload
    except UserProfile.DoesNotExist:
        raise exceptions.AuthenticationFailed('No bearer token found.')
