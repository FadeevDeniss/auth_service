import pytest
import requests

from api.models import UserProfile


class TestRegistration:
    _registration_url = 'http://127.0.0.1:8081/api/register/'

    @pytest.mark.parametrize('data, status_code', [
        ({'username': 'test_user_1', 'email': 'testmail@', 'password': 'testpwd12345'}, 400),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': ''}, 400),
        ({'username': 'test_user_1', 'email': '', 'password': 'testpwd12345'}, 400),
        ({'username': 'test_user_1', 'email': 'testmail@dev.com', 'password': 'test'}, 400),
        ({'username': '', 'email': '', 'password': ''}, 400),
        ({}, 400),
    ])
    def test_validation(self, data, status_code):
        response = requests.post(self._registration_url, json=data)
        assert response.status_code == status_code, f"Expected: {status_code}, Actual: {response.status_code}"

    @pytest.mark.django_db
    def test_user_exists_with_provided_email(self):
        existed_user = UserProfile.objects.create_user(
            username='test_user_1', email='testmail@dev.com', password='testpwd12345'
        )
        data = {'username': existed_user.username, 'email': existed_user.email, 'password': existed_user.password}
        response = requests.post(self._registration_url, json=data)
        assert response.status_code == 400, f"Expected: 400, Actual: {response.status_code}"

    def test_registration_success(self):
        expected_status_code = 201
        data = {'username': 'test_user_1', 'email': 'testmail2@dev.com', 'password': 'test12345!'}
        response = requests.post(self._registration_url, json=data)
        assert response.status_code == expected_status_code, (f"Expected: {expected_status_code},"
                                                              f" Actual {response.status_code} {response.json()}")