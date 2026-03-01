from .serializers import LetterSerializer, UserRegistrationSerializer
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
from rest_framework.parsers import MultiPartParser, FormParser


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
    
class LetterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        letters = Letter.objects.filter(user=request.user)
        serializer = LetterSerializer(letters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExecutorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Look for the executor assigned to the logged-in user
            executor = Executor.objects.get(user=request.user)
            return Response({
                "name": executor.name,
                "email": executor.email,
                "status": executor.status,
                "relationship": executor.relationship
            })
        except Executor.DoesNotExist:
            # Return 404 so the frontend knows to show the "Assign" form
            return Response({"message": "No executor assigned"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # update_or_create ensures one user only has one executor
        executor, created = Executor.objects.update_or_create(
            user=request.user,
            defaults={
                "name": request.data.get('name'),
                "email": request.data.get('email'),
                "phone": request.data.get('phone'),
                "relationship": request.data.get('relationship'),
            }
        )
        return Response({"message": "Executor assigned successfully"}, status=status.HTTP_201_CREATED)
    
class ExecutorVerificationView(APIView):
    # This must be AllowAny because the Executor doesn't have a user account yet
    permission_classes = [AllowAny] 
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        email = request.data.get('email')
        try:
            executor = Executor.objects.get(email=email, status='Verification_Pending')
            
            if 'document' in request.FILES:
                executor.verification_document = request.FILES['document']
                executor.is_verified = False # Admin must manually verify this in Admin Panel
                executor.save()
                return Response({"message": "Documents uploaded. Admin will verify shortly."}, status=status.HTTP_200_OK)
            
            return Response({"error": "No document provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Executor.DoesNotExist:
            return Response({"error": "Invalid request or unauthorized email."}, status=status.HTTP_404_NOT_FOUND)