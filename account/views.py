from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class TestView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        return Response({'message': 'Request Success!'})

    def post(self, request):
        pass
