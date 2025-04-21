from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from api.views.auth import RegistrationView, LoginView, RefreshTokenView
from api.views.common import MockAPIView

urlpatterns = [
    path('register/', csrf_exempt(RegistrationView.as_view()), name='registration'),
    path('login/', csrf_exempt(LoginView.as_view()), name='login'),
    path('refresh_token/', csrf_exempt(RefreshTokenView.as_view()), name='refresh_token'),
    path('transactions/', csrf_exempt(MockAPIView.as_view())),
]
