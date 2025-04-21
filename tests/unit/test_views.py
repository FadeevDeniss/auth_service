import pytest
from django.urls import reverse

from rest_framework import status


class TestRegistration:
    _registration_url = reverse('registration')

    @pytest.mark.parametrize('data, status_code', [
        ({'username': 'test_user_1', 'email': 'testmail@', 'password': 'testpwd12345'}, 400),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': ''}, 400),
        ({'username': 'test_user_1', 'email': '', 'password': 'testpwd12345'}, 400),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': 'test'}, 400),
        ({'username': '', 'email': '', 'password': ''}, 400),
        ({}, 400),
    ])
    def test_validation_error_returns_400(self, data, status_code, factory, registration_view):

        request = factory.post(self._registration_url, json=data)
        response = registration_view(request)

        assert response.status_code == status_code, f"Expected: {status_code}, Actual: {response.status_code}"

    @pytest.mark.django_db(transaction=True)
    def test_user_exists_returns_400(self, factory, registration_view, created_user):

        expected_status_code = status.HTTP_400_BAD_REQUEST
        data = {'username': created_user.username, 'email': created_user.email, 'password': created_user.password}

        request = factory.post(self._registration_url, data=data)
        response = registration_view(request)

        assert response.status_code == expected_status_code, \
            f"Expected: {expected_status_code}, Actual: {response.status_code}"

    @pytest.mark.django_db(transaction=True)
    def test_registration_success_returns_201(self, factory, registration_view):

        expected_status_code = status.HTTP_201_CREATED
        data = {'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': 'test12345!'}

        request = factory.post(self._registration_url, data=data)
        response = registration_view(request)

        assert response.status_code == expected_status_code, \
            f"Expected: {expected_status_code}, Actual: {response.status_code}."


class TestLoginView:

    _login_url = reverse('login')
    pytestmark = pytest.mark.django_db

    def test_user_not_registered_returns_400(self, factory, login_view):
        expected_status_code = status.HTTP_403_FORBIDDEN
        data = {'email': 'test_user@email.com', 'password': 'secret12345!'}

        request = factory.post(self._login_url, data=data)
        response = login_view(request)

        assert response.status_code == expected_status_code, \
            f"Expected: {expected_status_code}, Actual: {response.status_code}"

    def test_login_view_success_returns_200(self, factory, login_view, created_user):
        expected_status_code = status.HTTP_200_OK

        data = {'email': created_user.email, 'password': 'secret12345!'}

        request = factory.post(self._login_url, data=data)
        response = login_view(request)

        assert response.status_code == expected_status_code, \
            f"Expected: {expected_status_code}, Actual: {response.status_code}"
