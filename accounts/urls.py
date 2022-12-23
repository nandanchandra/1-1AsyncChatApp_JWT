from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from accounts.views import (
    CreateUserAPIView,
    MyTokenObtainPairView
)
urlpatterns = [
    path("create/user/",CreateUserAPIView.as_view(),name="create-user"),
    path('login/', MyTokenObtainPairView.as_view(), name='custom-token'),
    path('refresh/token/', TokenRefreshView.as_view(), name='token-refresh'),
]
