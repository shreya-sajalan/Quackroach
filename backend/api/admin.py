from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # The columns shown on the main user list page
    list_display = ('email', 'full_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Adds a search bar to find users by email or name
    search_fields = ('email', 'full_name')
    
    # Adds a filter sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    # Default ordering (newest users first)
    ordering = ('-date_joined',)
    
    # Grouping the fields nicely on the user edit page
    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def save_model(self, request, obj, form, change):
        """
        This is a crucial step for custom user models. 
        It ensures that if you type a new password in the admin panel, 
        Django actually encrypts/hashes it before saving it to the database.
        """
        if obj.pk:
            # Updating an existing user: Check if the password was changed
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            # Creating a brand new user: Hash the plain-text password
            obj.set_password(obj.password)
            
        super().save_model(request, obj, form, change)