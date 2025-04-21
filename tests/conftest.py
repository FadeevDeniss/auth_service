import pytest
from rest_framework.test import APIClient, APIRequestFactory

from api.models import UserProfile
from api.views.auth import RegistrationView, LoginView


@pytest.fixture(scope="session")
def client():
    return APIClient()


@pytest.fixture(scope='module')
def factory():
    return APIRequestFactory()


@pytest.fixture(scope='module')
def registration_view():
    return RegistrationView.as_view()


@pytest.fixture(scope='module')
def login_view():
    return LoginView.as_view()


@pytest.fixture(scope='module')
def created_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return UserProfile.objects.create_user(
            username='test_user',
            email='testuser01@mail.com',
            password="secret12345!"
        )
