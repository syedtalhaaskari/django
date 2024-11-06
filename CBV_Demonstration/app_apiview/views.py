from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer

class CategoryCreateListAPIView(APIView):
    def get(self, request):
        params = self.request.query_params
        name = params.get('name')
        id = params.get('id')

        category_objects = Category.objects
        
        if name is not None:
            category_objects = category_objects.filter(name=name)
        if id is not None:
            category_objects = category_objects.filter(id=id)
        
        categories = category_objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=self.request.data)

        if serializer.is_valid():
            Category.objects.create(**serializer.validated_data)

            return Response("Success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryRetrieveUpdateDestroy(APIView):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)

        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        category = Category.objects.get(pk=pk)

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(category, key, value)
            category.save()

            serializer = CategorySerializer(category)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)

        category.delete()

        return Response("Deleted", status=status.HTTP_200_OK)