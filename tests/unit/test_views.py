import pytest
from django.urls import reverse

from rest_framework import status


class TestRegistration:
    _registration_path = reverse('registration')

    @pytest.mark.parametrize('data, status_code', [
        ({'username': 'test_user_1', 'email': 'testmail@', 'password': 'testpwd12345'}, 400),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': ''}, 400),
        ({'username': 'test_user_1', 'email': '', 'password': 'testpwd12345'}, 400),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': 'test'}, 400),
        ({'username': '', 'email': '', 'password': ''}, 400),
        ({}, 400),
    ])
    def test_validation_error_returns_400(self, data, status_code, factory, registration_view):
        request = factory.post(self._registration_path, json=data)
        response = registration_view(request)
        assert response.status_code == status_code, \
            f"Expected: {status_code}, Actual: {response.status_code}"

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('data, status_code', [
        ({'username': 'test_user', 'email': 'testuser01@mail.com', 'password': 'secret12345!'},
         status.HTTP_400_BAD_REQUEST),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': 'test12345!'}, status.HTTP_201_CREATED)
    ])
    def test_user_registration_status_code(self, data, status_code, factory, registration_view, created_user):
        request = factory.post(self._registration_path, data=data)
        response = registration_view(request)
        assert response.status_code == status_code, \
            f"Expected: {status_code}, Actual: {response.status_code}"


class TestLoginView:

    _login_path = reverse('login')
    pytestmark = pytest.mark.django_db

    @pytest.mark.parametrize('data, status_code', [
        ({'email': 'test_user@email.com', 'password': 'secret12345!'}, status.HTTP_403_FORBIDDEN),
        ({'email': 'testuser01@mail.com', 'password': 'secret12345!'}, status.HTTP_200_OK),
    ])
    def test_user_login_status_code(self, data, status_code, factory, login_view, created_user):
        request = factory.post(self._login_path, data=data)
        response = login_view(request)
        assert response.status_code == status_code, \
            f"Expected: {status_code}, Actual: {response.status_code}"
