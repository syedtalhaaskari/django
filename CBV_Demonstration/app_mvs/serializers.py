from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Product, Supplier

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        many=True,
        allow_empty=False,
        write_only=True,
    )

    # category_id = serializers.IntegerField(write_only=True)
    # supplier_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = "__all__"  # This will include all fields from the Product model
        # fields = [
        #     "id",
        #     "category",
        #     "supplier",
        #     "name",
        #     "description",
        #     "price",
        #     "category_id",
        #     "supplier_id",
        # ]
    
    # def create(self, validated_data):
    #     supplier = validated_data.pop("supplier_id")
    #     category = validated_data.pop("category_id")

    #     product = Product.objects.create(**validated_data, category=category)
    #     product.supplier.set(supplier)

    #     return product