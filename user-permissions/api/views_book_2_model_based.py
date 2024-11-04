from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Book
from .serializers import BookSerializer
from .permissions import IsAuthor

@api_view(['GET'])
@permission_classes([AllowAny]) # allow accessing this API publically (without auth)
def get_all_books(requst: Request):
    categories = Book.objects.all()
    serializer = BookSerializer(categories, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthor]) # Check model-level permissions
def create_book(request: Request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        data['author_id'] = request.user.id
        Book.objects.create(**data)
        return Response("Success", status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthor])  # problem: any user that have the role 'author' can delete post of itself as well as the others
def delete_book(requst: Request, id):
    try:
        book = Book.objects.get(pk=id)

        book.delete()
        return Response("successfully deleted", status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response("Invalid Book", status=status.HTTP_404_NOT_FOUND)
