from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Letter, Vault

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # write_only ensures the password is never sent back in the API response
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')

    def create(self, validated_data):
        # create_user is crucial here—it automatically hashes the password!
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user
    
class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = ["ciphertext", "iv", "salt","item_count"]

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ["id", "recipient", "ciphertext", "iv", "salt", "created_at"]