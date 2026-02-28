from .serializers import UserRegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
        }
        return data
    
@api_view(['GET'])
def test_vault_data(request):
    mock_data = [
        {"id": 1, "title": "Chase Savings", "value": "$24,500", "type": "Bank"},
        {"id": 2, "title": "Life Insurance", "value": "$500,000", "type": "Insurance"},
    ]
    return Response({"message": "Connection successful!", "vault_items": mock_data})

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    # AllowAny is required so unauthenticated users can actually reach the signup page
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

class LoginView(TokenObtainPairView):
    """
    Takes an email and password, checks the database, 
    and returns an access token, refresh token, and user data.
    """
    serializer_class = CustomLoginSerializer