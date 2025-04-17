import json

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.auth_classes import JWTAuthentication


class MockAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return HttpResponse(json.dumps({'success': True}), status=200)
