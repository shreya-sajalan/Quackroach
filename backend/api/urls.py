from django.urls import path
from . import views
from .views import ExecutorVerificationView, LetterView, LoginView, RegisterUserView, VaultView ,ExecutorView


urlpatterns = [
    
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('vault/', VaultView.as_view(), name='vault'),
    path('letters/', LetterView.as_view(), name='letters'),
    path('executor/', ExecutorView.as_view(), name='executor'),
    path('verify-executor/', ExecutorVerificationView.as_view(), name='verify_executor'),
]