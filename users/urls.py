from django.urls import path,include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('signup/', views.Signupview.as_view(), name='signupview'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='loginview'),
    path('<int:id>/', views.UserView.as_view(), name='userview')
]