from django.urls import path
from . import views
from .views import LoginView, RegisterUserView 


urlpatterns = [
    path('test/', views.test_vault_data, name='test_vault'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    
]