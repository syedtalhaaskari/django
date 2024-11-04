from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import create_or_get_users, create_or_get_posts, login_view
# from .views import create_or_get_users


urlpatterns = [
    path("users/", create_or_get_users),
    path("posts/", create_or_get_posts),

    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]