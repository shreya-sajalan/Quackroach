from .serializers import UserRegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Security is BACK ON.
def dashboard_stats(request):
    # 1. Grab the REAL user that made the request
    user = request.user
    
    # Grab the exact full_name field from your custom models.py
    full_name = user.full_name
    
    # Calculate their last check-in using Django's built-in auth fields
    last_seen_date = user.last_login or user.date_joined
    last_check_in = last_seen_date.strftime("%b %d, %Y") if last_seen_date else "Just now"

    # ------------------------------------------------------------------
    # 2. REAL DATABASE QUERIES (For when you create the other models)
    # Once you build your Vault/Letter models, uncomment these lines!
    # ------------------------------------------------------------------
    # vault_count = VaultItem.objects.filter(user=user).count()
    # letter_count = Letter.objects.filter(user=user).count()
    # has_exec = Executor.objects.filter(user=user, status='Active').exists()
    
    # Setting these to 0 for now since the models don't exist yet.
    vault_count = 0
    letter_count = 0
    has_exec = False
    
    # Base score of 10% just for creating an account!
    completion_score = 10 

    return Response({
        "fullname": full_name,
        "completionPercentage": completion_score,
        "vaultItemsCount": vault_count,
        "lettersCount": letter_count,
        "hasExecutor": "Yes" if has_exec else "No",
        "lastCheckIn": last_check_in
    })