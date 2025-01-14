from django.urls import path
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, LogOutView,CollegeListView,CustomTokenObtainPairView

urlpatterns = [
    path('', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # Login using JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the access token
    path('logout/', LogOutView.as_view(), name='logout'),
    path('college-data/',CollegeListView.as_view(), name='college-data'),
]
