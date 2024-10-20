from rest_framework import serializers

from .category import CategorySerializer

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    category = CategorySerializer(read_only=True, many=True)
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

class ProductCategorySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )