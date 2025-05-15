from rest_framework import serializers

from api.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    username = None
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    class Meta:
        model = UserProfile
        fields = ['email', 'password']


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
