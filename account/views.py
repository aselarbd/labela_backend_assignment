from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import SignUpSerializer
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["User API"])
    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            new_account = serializer.save()
            response = serializer.data
            response["token"] = Token.objects.get(user=new_account).key

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    @extend_schema(tags=["User API"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["User API"])
    def post(self, request: Request):
        request.user.auth_token.delete()
        response = {"message": "Logged out successfully"}
        return Response(data=response, status=status.HTTP_200_OK)
