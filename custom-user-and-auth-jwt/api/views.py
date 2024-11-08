from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from .models import User

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_or_get_users(request: Request):
    if request.method == 'GET':
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # User can login and act as an administrator with full control
        User.objects.create(
            dob="1994-08-25",
            email="danish@gmail.com", 
            password=make_password("admin"),
            is_staff=True,            # Grants access to the admin interface
            is_superuser=True         # Grants all permissions and unrestricted access
        )

        # User can only login to the admin, but can only perform actions they have specific permissions for
        user = User(
            dob="1994-08-25",
            email="fahad@gmail.com", 
            is_staff=True              # Grants access to the admin interface, but permissions are needed for specific actions
        )
        user.set_password("admin")      # Securely hashes and sets the password
        user.save()

        # Improper configuration: This user cannot log in to the admin because 'is_staff' is missing
        User.objects.create(
            dob="1994-08-25",
            email="shoaib@gmail.com", 
            password=make_password("admin"),
            is_superuser=True          # Grants all permissions, but without 'is_staff', they cannot log in
        )
        
        users = "success"

        return Response(users, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def create_or_get_posts(request: Request):
    if request.user.is_authenticated == False:
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
    data = {
        "is_authenticated": request.user.is_authenticated,
        "is_staff": request.user.is_staff,
        "is_superuser": request.user.is_superuser,
        "email": request.user.email,
        "dob": request.user.dob,
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request: Request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token)
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)