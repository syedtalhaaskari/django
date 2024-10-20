from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from app_1.models.category import Category as category_model
from app_1.serializers.category import CategorySerializer

@api_view(['GET','POST'])
def create_or_get_categories(request: Request):
    if request.method == 'GET':
        customers = category_model.objects.all()
        serializer = CategorySerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_model.objects.create(**serializer.validated_data)

            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)