from django.urls import path

from .views import (
    MyObtainTokenPairView,
    RegisterView,
    UsersListView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('users/', UsersListView.as_view(), name='users'),
]
