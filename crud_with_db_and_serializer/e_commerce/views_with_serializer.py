from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Category as category_model
from .serializers import CategorySerializer

@api_view(['GET', 'POST'])
def get_categories_or_create_category(request: Request):
    if request.method == 'GET':
        params = request.query_params
        category_objects = category_model.objects

        name = params.get('name')
        if name is not None:
            category_objects = category_objects.filter(name=name)
        
        id = params.get('id')
        if id is not None:
            category_objects = category_objects.filter(id=id)

        categories = category_objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_model.objects.create(**serializer.validated_data)

            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_category(request: Request, id):
    category = category_model.objects.get(pk=id)

    if request.method == 'GET':
        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(category, key, value)
            category.save()
            serializer = CategorySerializer(category)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        category.delete()

        return Response("Deleted", status=status.HTTP_200_OK)