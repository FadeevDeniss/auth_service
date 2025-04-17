from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.crypto_utils import generate_jwt_keypair, verify_jwt_token
from api.models import UserProfile
from api.serializers import CreateUserSerializer
from auth_service.redis import blacklist as b


class RegistrationView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserProfile.objects.filter(email=serializer.validated_data['email'])

        if user.exists():
            return Response(
                {
                    'success': False,
                    'error': f'User with {serializer.validated_data["email"]} already exists.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = serializer.save()
        token, refresh_token = generate_jwt_keypair(new_user.pk)

        return Response(
            {
                'success': True,
                'access_token': token,
                'refresh_token': refresh_token
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    def post(self, request):
        user = authenticate(username=request.data['email'], password=request.data['password'])

        if user is not None:
            access_token, refresh_token = generate_jwt_keypair(user.pk)

            return Response(
                {
                    'success': True,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'success': False,
                'error': 'No user with provided email and password.'
            },
            status=status.HTTP_403_FORBIDDEN
        )


class RefreshTokenView(APIView):

    def post(self, request):
        token = request.data.get('refresh_token')

        if not token:
            return Response(
                {
                    'success': False,
                    'error': 'No refresh token provided.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user, payload = verify_jwt_token(token, settings.REFRESH_TOKEN_SECRET)

        if b.get(payload['jti']) is not None:
            return Response(
                {
                    'success': False,
                    'error': 'Token is cancelled.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        b.set(payload['jti'], 1)
        refresh_token_expire_at = int(settings.REFRESH_TOKEN_LIFETIME)
        b.expireat(
            payload['jti'],
            int((datetime.now() + timedelta(seconds=refresh_token_expire_at)).timestamp()))

        access_token, refresh_token = generate_jwt_keypair(user.pk)

        return Response(
            {
                'success': False,
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            status=status.HTTP_200_OK
        )
