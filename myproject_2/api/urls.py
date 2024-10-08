from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.create_and_get_all_users),
    path("users/<int:id>/", views.get_update_and_delete_user)
]