from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import AccountRegistrationSerializer


# Create your views here.
class TestView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        return Response({'message': 'Request Success!'})

    def post(self, request):
        pass


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
