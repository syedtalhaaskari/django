from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_books(request: Request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_book(request: Request): # problem: all logged in user can create posts
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        data=serializer.validated_data
        data['author_id'] = request.user.id
        Book.objects.create(**data)
        return Response("success", status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_book(requst: Request, id):
    
    book = Book.objects.get(pk=id)
    
    book.delete()
    
    return Response("Successfully Deleted", status=status.HTTP_200_OK)