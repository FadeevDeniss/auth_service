import uuid

from datetime import timedelta, datetime

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError


def sign_jwt(pk, secret, exp: int = 3600, alg: str = 'HS256'):

    issued_at = datetime.now()
    expires = issued_at + timedelta(seconds=int(exp))
    token_id = str(uuid.uuid4())

    payload = {
        'id': pk,
        'jti': token_id,
        'iat': round(issued_at.timestamp()),
        'exp': round(expires.timestamp())
    }
    return encode(payload, secret, algorithm=alg, sort_headers=True)


def verify_jwt(token: str, secret: str):
    try:
        payload = decode(token, secret, algorithms=['HS256'])
    except (ExpiredSignatureError, InvalidTokenError):
        return None
    return payload
