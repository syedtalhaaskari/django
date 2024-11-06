from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import SignupSerializer, LoginSerializer, UserSerializer

@api_view(['POST'])
def signup_view(request: Request):
    data = request.data
    serializer = SignupSerializer(data = data)

    if serializer.is_valid():
        data = serializer.validated_data

        data['password'] = make_password(data['password'])

        User.objects.create(**data)
        return Response("User created successfully", status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login_view(request: Request):
    data = request.data
    
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.validated_data

        user = authenticate(
            request=request, username=data['username'], email=data['email']
        )

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    return Response("Invalid Data", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request: Request):
    logout(request)

    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def profile_view(request: Request):
    if request.user.is_authenticated:
        user = UserSerializer(request.user)
        return Response(user.data)
    else:
        return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)