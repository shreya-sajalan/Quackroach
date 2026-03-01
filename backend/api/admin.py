from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from datetime import timedelta
from django.utils.safestring import mark_safe

from .models import Vault, Letter, Executor

User = get_user_model()

# --- Custom User Admin ---

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_active', 'check_in_status', 'date_joined')
    search_fields = ('email', 'full_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'full_name'),
        }),
    )

    def check_in_status(self, obj):
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
    list_display = ('user', 'item_count', 'updated_at')
    readonly_fields = ('ciphertext', 'iv', 'salt')
    search_fields = ('user__email', 'user__full_name')


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'user', 'created_at')
    readonly_fields = ('ciphertext', 'iv', 'salt')
    search_fields = ('recipient', 'user__email')


# --- Executor System ---

@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'user', 'status', 'is_verified', 'view_document')
    list_editable = ('status', 'is_verified')
    readonly_fields = ('view_document',)
    search_fields = ('name', 'email', 'user__email')
    
    # Registered dual actions for the dropdown menu
    actions = [
        'trigger_deadman_notification',
        'trigger_access_granted_manual'
    ]

    # 1. Custom Field: View Uploaded Document
    def view_document(self, obj):
        if obj.verification_document:
            return mark_safe(f'<a href="{obj.verification_document.url}" target="_blank" style="color: #E5B869; font-weight: bold;">View Proof</a>')
        return "No Upload"
    view_document.short_description = 'Verification File'

    # 2. Automated Action: Send Access Email on Status Change
    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Executor.objects.get(pk=obj.pk)
            # Trigger email only when status moves to Access_Granted and is_verified is checked
            if old_obj.status != 'Access_Granted' and obj.status == 'Access_Granted' and obj.is_verified:
                self.send_access_granted_email(obj)
        super().save_model(request, obj, form, change)

    def send_access_granted_email(self, executor):
        subject = f"Final Access Granted: {executor.user.full_name}'s Legacy"
        context = {
            'executor_name': executor.name,
            'user_name': executor.user.full_name,
            'login_email': executor.user.email,
            'site_url': 'http://localhost:5173/unlock-legacy'
        }
        html_content = render_to_string('emails/access_granted.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, None, [executor.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    # 3. Manual Action: Trigger Initial Notification
    @admin.action(description="Force Send Dead-Man Notification")
    def trigger_deadman_notification(self, request, queryset):
        success_count = 0
        for executor in queryset:
            try:
                subject = f"Security Protocol Initiated: {executor.user.full_name}"
                context = {
                    'executor_name': executor.name,
                    'user_name': executor.user.full_name,
                    'site_url': 'http://localhost:5173/executor-portal'
                }
                html_content = render_to_string('emails/deadman_notification.html', context)
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, None, [executor.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                executor.status = 'Verification_Pending'
                executor.save()
                success_count += 1
            except Exception as e:
                self.message_user(request, f"Error sending to {executor.name}: {str(e)}", level='error')
        
        self.message_user(request, f"Sent {success_count} initial notifications successfully.")

    # 4. Manual Action: Trigger Access Granted Email
    @admin.action(description="Force Send Access Granted Email")
    def trigger_access_granted_manual(self, request, queryset):
        success_count = 0
        for executor in queryset:
            if executor.is_verified and executor.status == 'Access_Granted':
                try:
                    self.send_access_granted_email(executor)
                    success_count += 1
                except Exception as e:
                    self.message_user(request, f"Error sending to {executor.name}: {str(e)}", level='error')
            else:
                self.message_user(request, f"Skipped {executor.name}: Status must be 'Access_Granted' and 'Is verified' must be checked.", level='warning')
        
        if success_count > 0:
            self.message_user(request, f"Sent {success_count} final access emails successfully.")