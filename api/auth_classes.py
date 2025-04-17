from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header
from django.conf import settings

from api.crypto_utils import verify_jwt_token


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'bearer':
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid header. No token provide.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid Bearer header. Token string should not contain spaces.')

        user, _ = verify_jwt_token(auth[1], settings.ACCESS_TOKEN_SECRET)

        return user, None
