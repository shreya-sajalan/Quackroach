from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a standard User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
            
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        # set_password automatically hashes the password securely
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model where email is the unique identifier for authentication
    instead of usernames.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    
    # Required fields for Django's permission system and admin panel
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    # Tells Django to use 'email' for logging in instead of 'username'
    USERNAME_FIELD = 'email'
    
    # Fields required when creating a superuser via the terminal
    REQUIRED_FIELDS = ['full_name'] 

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
class Vault(models.Model):
    # OneToOne ensures a user can only ever have exactly ONE vault
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ciphertext = models.TextField()
    iv = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    item_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Encrypted Vault for {self.user.email}"
    
class Letter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    ciphertext = models.TextField(blank=True, null=True)
    iv = models.CharField(max_length=255, blank=True, null=True)
    salt = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Letter: {self.title} (by {self.user.email})"

class Executor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=100)
    verification_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)
    # Statuses: 'Active' (Alive), 'Verification_Pending' (Triggered), 'Access_Granted' (Confirmed)
    status = models.CharField(max_length=50, default='Active')
    is_verified = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Executor {self.name} for {self.user.email}"