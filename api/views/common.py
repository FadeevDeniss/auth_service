import json

from django.http import HttpResponse
from rest_framework.views import APIView


class MockAPIView(APIView):

    def get(self, request):
        return HttpResponse(json.dumps({'success': True}), status=200)
