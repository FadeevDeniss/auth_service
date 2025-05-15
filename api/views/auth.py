from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.crypto_utils import sign_jwt, verify_jwt
from api.models import UserProfile
from api.serializers import UserSerializer, TokenSerializer
from auth_service.redis import redis_storage as r


class RegistrationView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    view_name = 'registration'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserProfile.objects.filter(
            email=serializer.validated_data['email']
        )

        if user.exists():
            return Response(
                {
                    'success': False,
                    'error': f'User with {serializer.validated_data["email"]} already exists.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = UserProfile(
            email=serializer.validated_data['email']
        )
        new_user.set_password(serializer.validated_data['password'])
        new_user.save()

        access_token = sign_jwt(
            new_user.pk, settings.ACCESS_TOKEN_SECRET, settings.ACCESS_TOKEN_EXP
        )
        refresh_token = sign_jwt(
            new_user.pk, settings.REFRESH_TOKEN_SECRET, settings.REFRESH_TOKEN_EXP
        )

        return Response(
            {
                'success': True,
                'email': new_user.email,
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = UserSerializer
    view_name = 'login'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user is not None:
            access_token = sign_jwt(
                user.pk, settings.ACCESS_TOKEN_SECRET, settings.ACCESS_TOKEN_EXP
            )
            refresh_token = sign_jwt(
                user.pk, settings.REFRESH_TOKEN_SECRET, settings.REFRESH_TOKEN_EXP
            )

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
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer
    view_name = 'refresh_token'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = verify_jwt(
            serializer.initial_data['refresh_token'],
            settings.REFRESH_TOKEN_SECRET
        )
        if not payload:
            return Response(
                {
                    'success': False,
                    'error': 'Token expired or invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            user = UserProfile.objects.get(id=payload['id'])
        except UserProfile.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if r.get(payload['jti']) is not None:
            return Response(
                {
                    'success': False,
                    'error': 'Token is cancelled'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        exp_at = datetime.now() + timedelta(settings.REFRESH_TOKEN_EXP)
        r.set(payload['jti'], 1)
        r.expireat(
            payload['jti'],
            round(int(exp_at.timestamp()))
        )
        access_token = sign_jwt(
            user.pk, settings.ACCESS_TOKEN_SECRET, settings.ACCESS_TOKEN_EXP)
        refresh_token = sign_jwt(
            user.pk, settings.REFRESH_TOKEN_SECRET, settings.REFRESH_TOKEN_EXP)

        return Response(
            {
                'success': True,
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            status=status.HTTP_200_OK
        )
