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
from rest_framework import status
from .models import Vault
from .serializers import VaultSerializer
from rest_framework.views import APIView
from .models import Vault, Letter, Executor

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
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    # 1. Get real Vault count
    try:
        vault = Vault.objects.get(user=user)
        vault_count = vault.item_count
    except Vault.DoesNotExist:
        vault_count = 0
        
    # 2. Get real Letter count
    letter_count = Letter.objects.filter(user=user).count()
    
    # 3. Check if they have at least one active or pending Executor
    has_exec = Executor.objects.filter(user=user).exists()
    
    # Calculate Completion Score dynamically based on their progress!
    completion_score = 10 # Base score for signing up
    if vault_count > 0: completion_score += 40
    if letter_count > 0: completion_score += 20
    if has_exec: completion_score += 30
    
    # Format the user's name gracefully
    full_name = user.full_name if hasattr(user, 'full_name') and user.full_name else user.username
    last_seen_date = user.last_login or user.date_joined
    last_check_in = last_seen_date.strftime("%b %d, %Y") if last_seen_date else "Just now"

    return Response({
        "fullname": full_name,
        "completionPercentage": completion_score,
        "vaultItemsCount": vault_count,
        "lettersCount": letter_count,
        "hasExecutor": "Yes" if has_exec else "No",
        "lastCheckIn": last_check_in
    })

class VaultView(APIView):
    permission_classes = [IsAuthenticated] # Bouncer is active

    def get(self, request):
        try:
            vault = Vault.objects.get(user=request.user)
            serializer = VaultSerializer(vault)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vault.DoesNotExist:
            # If the user is new and hasn't saved anything yet, return a clean empty state
            return Response({"message": "Vault not initialized"}, status=status.HTTP_200_OK)

    def post(self, request):
        # Fetch the existing vault, or create a blank one if it's their first time
        vault, created = Vault.objects.get_or_create(user=request.user)
        
        # Pass the instance to the serializer so it UPDATES instead of duplicating
        serializer = VaultSerializer(vault, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)