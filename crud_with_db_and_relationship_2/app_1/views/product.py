from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from app_1.models.product import Product as product_model
from app_1.models.category import Category as category_model
from app_1.serializers.product import ProductSerializer, ProductCategorySerializer

@api_view(['GET', 'POST'])
def create_or_get_products(request: Request):
    if request.method == 'GET':
        products = product_model.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            cat_ids = serializer.validated_data.pop('category_ids')

            db_categories = category_model.objects.filter(id__in=cat_ids).all()
            if len(db_categories) != len(cat_ids):
                return Response("One or more category IDS are invalid.", status=status.HTTP_400_BAD_REQUEST)
            
            product = product_model.objects.create(**serializer.validated_data)
            product.category.set(cat_ids)

            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST', 'GET'])
def assign_categories(request: Request):
    if request.method == 'GET':
        customers = product_model.objects.prefetch_related("category").all()
        serializer = ProductSerializer(customers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.pop('product_id')
            cat_ids = serializer.validated_data.pop('category_ids')

            db_categories = category_model.objects.filter(id__in=cat_ids).all()
            if len(db_categories) != len(cat_ids):
                return Response("One or more category IDS are invalid.", status=status.HTTP_400_BAD_REQUEST)
            
            db_product = product_model.objects.filter(id=product_id).first()
            if db_product is None:
                return Response("Invalid product.", status=status.HTTP_400_BAD_REQUEST)
            
            db_product.category.set(cat_ids)
            return Response("Success", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)