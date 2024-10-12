from django.urls import path

from . import views

urlpatterns = [
    path('homepage/', views.homepage, name="posts_home"),
    path('', views.list_posts, name="list_posts"),
    path('<int:post_index>', views.post_details, name="post_details"),
]