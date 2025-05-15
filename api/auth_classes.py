from rest_framework import authentication, exceptions, status
from django.conf import settings

from api.crypto_utils import verify_jwt
from api.models import UserProfile


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth_data or auth_data[0].lower() != 'jwt':
            return None
        if len(auth_data) == 1:
            raise exceptions.AuthenticationFailed(
                'Invalid header. No token provide.',
                status.HTTP_400_BAD_REQUEST
            )
        elif len(auth_data) > 2:
            raise exceptions.AuthenticationFailed(
                'Invalid Bearer header. Token string should not contain spaces.',
                status.HTTP_400_BAD_REQUEST
            )

        payload = verify_jwt(auth_data[1], settings.ACCESS_TOKEN_SECRET)

        if payload is None:
            raise exceptions.AuthenticationFailed('Token expired or invalid.', status.HTTP_401_UNAUTHORIZED)

        user = UserProfile.objects.filter(pk=payload['id'])

        if not user.exists():
            raise exceptions.AuthenticationFailed('No such user.', status.HTTP_404_NOT_FOUND)

        return user, None
