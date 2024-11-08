from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET', 'POST'])
def create_or_get_users(request: Request):
    if request.method == 'GET':
        data = User.objects.all()
        users = []
        for user in data:
            users.append({
                "email": user.email,
                "username": user.username,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            })
        return Response(users, status=status.HTTP_200_OK)
    if request.method == 'POST':
        # User can login and act as an administrator with full control
        User.objects.create(
            email="danish@gmail.com", 
            username="danish", 
            password=make_password("admin"),
            is_staff=True,            # Grants access to the admin interface
            is_superuser=True         # Grants all permissions and unrestricted access
        )


        # User can only login to the admin, but can only perform actions they have specific permissions for
        user = User(
            email="fahad@gmail.com", 
            username="fahad",
            is_staff=True              # Grants access to the admin interface, but permissions are needed for specific actions
        )
        user.set_password("admin")      # Securely hashes and sets the password
        user.save()



        # Improper configuration: This user cannot log in to the admin because 'is_staff' is missing
        User.objects.create(
            email="shoaib@gmail.com", 
            username="shoaib", 
            password=make_password("admin"),
            is_superuser=True          # Grants all permissions, but without 'is_staff', they cannot log in
        )
        
        users = "success"
        return Response(users, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def create_or_get_posts(request: Request):
    if request.user.is_authenticated == False:
        return Response("please login")
    
    data = {
        "is_authenticated": request.user.is_authenticated,
        "is_staff": request.user.is_staff,
        "is_superuser": request.user.is_superuser,
        "email": request.user.email,
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny]) # allow accessing this API publically (without auth)
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh_token = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh_token.access_token),
            "refresh_token": str(refresh_token)
            }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)