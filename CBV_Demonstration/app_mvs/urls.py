from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.product import ProductViewSet
from .views.category import (
    CategoryViewSet,
    CategoryMethodOverrideViewSet,  # override methods for PUT and DELETE requests
)
from .views.supplier import (
    SupplierListCreateAPIView, 
    SupplierRetrieveUpdateDestroyAPIView,
    SupplierMethodOverrideListCreateAPIView,
    SupplierMethodOverrideRetrieveUpdateDestroyAPIView,  # override methods for PUT and DELETE requests
    SupplierAllViews,  # a single view that handles all GET, PUT, DELETE requests
)

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet, basename="categories")
router.register("categories-override", CategoryMethodOverrideViewSet, basename="categories-override")

urlpatterns = [
    path("suppliers/", SupplierListCreateAPIView.as_view()),
    path("suppliers/<int:pk>", SupplierRetrieveUpdateDestroyAPIView.as_view()),
    # all common override methods
    path("suppliers-override/", SupplierMethodOverrideListCreateAPIView.as_view()),
    path(
        "suppliers-override/<int:pk>",
        SupplierMethodOverrideRetrieveUpdateDestroyAPIView.as_view(),
    ),
    # detail view will not work properly. You will need atleast 2 separate classes as above
    path("suppliers-one-class/", SupplierAllViews.as_view()),
    path("suppliers-one-class/<int:pk>", SupplierAllViews.as_view()),
] + router.urls