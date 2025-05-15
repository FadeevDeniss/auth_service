import pytest

from rest_framework.exceptions import ValidationError

from api.serializers import UserSerializer


class TestUserSerializer:
    serializer_class = UserSerializer

    @pytest.mark.parametrize('data, is_valid', [
        ({'username': '', 'email': 'testmail@', 'password': 'testpwd12345'}, False),
        ({'email': 'testmail@', 'password': 'testpwd12345'}, False),
        ({'email': 'testmail@dev.com', 'password': ''}, False),
        ({'email': '', 'password': 'testpwd12345'}, False),
        ({'email': 'testmail@dev.com', 'password': 'test'}, False),
        ({'email': '', 'password': ''}, False),
        ({'email': ''}, False),
        ({'password': ''}, False),
        ({}, False),
    ])
    def test_invalid_credentials_raises_validation_error(self, data, is_valid):
        serializer = self.serializer_class(data=data)
        validation_status = serializer.is_valid()

        assert is_valid == validation_status, f"Expected: {is_valid}, Actual: {validation_status}"

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
            pytest.fail(f"Should raise ValidationError.")

    def test_correct_credentials_serialization_valid(self, valid_credentials):
        serializer = self.serializer_class(data=valid_credentials)
        validation_status = serializer.is_valid(raise_exception=True)

        assert validation_status, f"Wrong result, expected: True, Actual: {validation_status}"
