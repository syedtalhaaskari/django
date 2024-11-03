from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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
        return Response({
            'refresh': str(refresh),
            'accesss': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'error':'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request: Request):
    return Response({'message': "Logged out successfully."}, status=status.HTTP_200_OK)