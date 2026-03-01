from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from datetime import timedelta

from .models import Vault, Letter, Executor

User = get_user_model()

# --- Custom User Admin ---

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Refined User Admin to handle the custom 'full_name' field
    and provide visual feedback on user activity.
    """
    list_display = ('email', 'full_name', 'is_staff', 'is_active', 'check_in_status', 'date_joined')
    search_fields = ('email', 'full_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)
    
    # Organize the user edit page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for creating a new user via Admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'full_name'),
        }),
    )

    def check_in_status(self, obj):
        """
        Calculates inactivity. Red if > 30 days, Green if active.
        """
        last_seen = obj.last_login or obj.date_joined
        if not last_seen:
            return format_html('<span style="color: #9ca3af;">No Data</span>')
        
        limit = timezone.now() - timedelta(days=30)
        formatted_date = last_seen.strftime("%b %d, %Y")
        
        if last_seen < limit:
            return format_html(
                '<span style="color: #f87171; font-weight: bold;">{} (Inactive)</span>',
                formatted_date
            )
        return format_html(
            '<span style="color: #4ade80;">{} (Active)</span>',
            formatted_date
        )

    check_in_status.short_description = 'Last Check-in'


# --- Legacy System Models ---

@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
    """Admin view for the Zero-Knowledge Vault."""
    list_display = ('user', 'item_count', 'updated_at')
    readonly_fields = ('ciphertext', 'iv', 'salt')
    search_fields = ('user__email', 'user__full_name')


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    """Admin view for Legacy Letters."""
    list_display = ('recipient', 'user', 'created_at')
    readonly_fields = ('ciphertext', 'iv', 'salt')
    search_fields = ('recipient', 'user__email')


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    """
    Admin view for the Executor system, including manual 
    trigger for the Dead-Man Switch notification.
    """
    list_display = ('name', 'relationship', 'user', 'status', 'is_verified')
    list_editable = ('status', 'is_verified')
    search_fields = ('name', 'email', 'user__email')
    actions = ['trigger_deadman_notification']

    @admin.action(description="Force Send Dead-Man Notification")
    def trigger_deadman_notification(self, request, queryset):
        """
        Sends the professional HTML email to selected Executors.
        """
        success_count = 0
        error_count = 0

        for executor in queryset:
            try:
                # 1. Prepare Content
                subject = f"Security Protocol Initiated: {executor.user.full_name}"
                context = {
                    'executor_name': executor.name,
                    'user_name': executor.user.full_name,
                    'site_url': 'http://localhost:5173' # Frontend URL
                }

                # 2. Render HTML & Text Fallback
                html_content = render_to_string('emails/deadman_notification.html', context)
                text_content = strip_tags(html_content)

                # 3. Create Email Object
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    None, # Uses DEFAULT_FROM_EMAIL from settings
                    [executor.email]
                )
                msg.attach_alternative(html_content, "text/html")
                
                # 4. Send
                msg.send()

                # 5. Update Status
                executor.status = 'Verification_Pending'
                executor.save()
                success_count += 1
            except Exception as e:
                self.message_user(request, f"Failed to send to {executor.name}: {str(e)}", level='error')
                error_count += 1

        if success_count > 0:
            self.message_user(request, f"Successfully sent {success_count} notifications.")
        if error_count == 0 and success_count > 0:
            self.message_user(request, "All selected notifications sent successfully.")