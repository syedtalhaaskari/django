from django.urls import path

from .views import CategoryCreateListAPIView, CategoryRetrieveUpdateDestroy

urlpatterns = [
    path("categories/", CategoryCreateListAPIView.as_view()),
    path("categories/<int:pk>", CategoryRetrieveUpdateDestroy.as_view()),
]