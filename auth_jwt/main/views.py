from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

@api_view(['GET'])
def user_detail_view(request):
    user = request.user
    if user.is_authenticated:
        return Response({"username": user.username, "email": user.email}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request: Request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Please provide both username and password."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response = Response()
        response.data = response_data
        response.status = status.HTTP_201_CREATED
        response.set_cookie(
            key='refresh_token',
            value=response_data['refresh'],
            secure=True,
            httponly=True,
        )
        response.set_cookie(
            key='access_token',
            value=response_data['access'],
            secure=True,
            httponly=True,
        )
        return response
    return Response({'error':'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request: Request):
    try:
        refresh_token = request.data.get('refresh')

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'detail': "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request: Request):
    try:
        data = request.data
        user_obj = {
            'username': data['username'],
            'password': data['password'],
        }

        # Creating a User and Password Using set_password()
        # user = User(
        #     username=user_obj['username'],
        # )
        # user.set_password(user_obj['password'])
        # user.save()

        # Using make_password() to Manually Hash a Password
        user_obj['password'] = make_password(user_obj['password'])
        User.objects.create(**user_obj)

        return Response({ 'success': user_obj }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)