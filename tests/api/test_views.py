import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import UserProfile


pytestmark = [pytest.mark.smoke, pytest.mark.django_db]


@pytest.fixture(scope='class')
def factory():
    return APIRequestFactory()


class TestRegistration:

    _registration_url = reverse('registration')

    def test_account_created_after_registration(self, factory, registration_view, valid_credentials):
        request = factory.post(self._registration_url, data=valid_credentials)
        response = registration_view(request)

        assert UserProfile.objects.count() == 1, f"Wrong profiles count, user is not created"
        assert UserProfile.objects.get().email == response.data['email'], \
            f"Email not equal to {valid_credentials['email']}"

    def test_user_already_registered_return_400(self, factory, registration_view, valid_credentials, created_user):
        request = factory.post(self._registration_url, data=valid_credentials)
        response = registration_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, \
            f"Expected: {status.HTTP_400_BAD_REQUEST}, Actual: {response.status_code}"

    def test_registration_success_returns_correct_response(self, factory, registration_view, valid_credentials):
        request = factory.post(self._registration_url, data=valid_credentials)
        response = registration_view(request)
        response_length = len(response.data)

        assert response_length == 4, f"Wrong response length, expected 4, actual: {response_length}"
        assert response.data['success'], \
            f"Wrong response status text, expected: True, actual: {response.data['success']}"

    def test_registration_success_return_201(self, factory, registration_view, valid_credentials):
        request = factory.post(self._registration_url, data=valid_credentials)
        response = registration_view(request)

        assert response.status_code == status.HTTP_201_CREATED, \
            f"Expected: {status.HTTP_201_CREATED}, Actual: {response.status_code}."


class TestLoginView:

    _login_url = reverse('login')

    def test_login_unregistered_user_return_403(self, factory, login_view, valid_credentials):
        request = factory.post(self._login_url, data=valid_credentials)
        response = login_view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            f"Expected: {status.HTTP_403_FORBIDDEN}, Actual: {response.status_code}"

    def test_login_success_return_200(self, factory, login_view, created_user, valid_credentials):
        expected_status_code = status.HTTP_200_OK

        request = factory.post(self._login_url, data=valid_credentials)
        response = login_view(request)
        response_len = len(response.data)

        assert response.status_code == expected_status_code, \
            f"Expected: {expected_status_code}, Actual: {response.status_code}"
        assert response_len == 3, f"Wrong response length: {response_len}"


class TestRefreshTokenView:

    _registration_url = reverse('refresh_token')

    def test_invalid_refresh_token_return_401(self, factory, token, invalid_refresh_token, refresh_token_view):
        request = factory.post(
            self._registration_url,
            data={'refresh_token': invalid_refresh_token},
            headers={'Authorization': f'JWT {token}'}
        )
        response = refresh_token_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            f"Expected: {status.HTTP_401_UNAUTHORIZED}, Actual: {response.status_code}"

    def test_refresh_token_with_wrong_pk_return_404(self, factory, token, refresh_token_invalid_pk,
                                                    refresh_token_view):
        request = factory.post(
            self._registration_url,
            data={'refresh_token': refresh_token_invalid_pk},
            headers={'Authorization': f'JWT {token}'}
        )
        response = refresh_token_view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            f"Expected: {status.HTTP_404_NOT_FOUND}, Actual: {response.status_code}"

    def test_expired_refresh_token_return_401(self, factory, token, expired_refresh_token,
                                              refresh_token_view):
        request = factory.post(
            self._registration_url,
            data={'refresh_token': expired_refresh_token},
            headers={'Authorization': f'JWT {token}'}
        )
        response = refresh_token_view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            f"Expected: {status.HTTP_401_UNAUTHORIZED}, Actual: {response.status_code}"

    def test_refresh_success_return_200(self, factory, token, refresh_token, refresh_token_view):
        request = factory.post(
            self._registration_url,
            data={'refresh_token': refresh_token},
            headers={'Authorization': f'JWT {token}'}
        )
        response = refresh_token_view(request)

        assert response.status_code == status.HTTP_200_OK, \
            f"Expected: {status.HTTP_200_OK}, Actual: {response.status_code}"

    @pytest.mark.usefixtures('redis_add_document')
    def test_second_try_with_used_token_return_404(self, factory, token, refresh_token, refresh_token_view):
        request = factory.post(
            self._registration_url,
            data={'refresh_token': refresh_token},
            headers={'Authorization': f'JWT {token}'}
        )
        response = refresh_token_view(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            f"Wrong status code, expected: {status.HTTP_404_NOT_FOUND}"
