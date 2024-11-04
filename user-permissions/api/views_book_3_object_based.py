from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import Book
from .serializers import BookSerializer
from .permissions import IsAuthor, IsReader, IsAuthorOrModerator

@api_view(['GET'])
@permission_classes([IsReader]) # allow accessing this API publically (without auth)
def get_all_books(request: Request):
    books = Book.objects.all()

    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthor])  # Check model-level permissions
def create_book(requst: Request): # only the user having group/role 'author' can create post
    serializer = BookSerializer(data=requst.data)
    if serializer.is_valid():
        data = serializer.validated_data
        data['author_id'] = requst.user.id
        Book.objects.create(**data)
        return Response("success", status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE']) 
@permission_classes([IsAuthorOrModerator])  # problem: permission doesn't auto trigger in FBV
def delete_book(request: Request, id):
    try:
        book = Book.objects.get(pk=id)

        # manually trigger the method because the automatic trigger only works with queryset and queryset is a feature of CBV
        # we are using FBV
        if not IsAuthorOrModerator().has_object_permission(request, None, book):
            return Response({"error": "You cannot delete other author books"}, status=status.HTTP_403_FORBIDDEN)

        book.delete()
        return Response("successfully deleted", status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response("Invalid Book", status=status.HTTP_404_NOT_FOUND)