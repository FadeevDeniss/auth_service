from rest_framework import serializers
from api.models import UserProfile


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
