from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AuthTokenSerializer, UserRegisterSerializer

User = get_user_model()


class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthToken(APIView):
    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise AuthenticationFailed()
