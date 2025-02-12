from django.contrib import admin
from .models import User, Organization

# Register the Organization model
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization_name', 'address', 'created_at', 'updated_at']
    search_fields = ['organization_name']
    list_filter = ['created_at']

admin.site.register(Organization, OrganizationAdmin)

# Register the User model
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone_number', 'organization', 'is_active', 'is_admin', 'is_staff']
    readonly_fields = ['username', 'email', 'phone_number']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_admin', 'is_staff', 'organization']
    list_editable = ['is_active']
    raw_id_fields = ['organization']  # To use a more efficient dropdown for ForeignKey fields


admin.site.register(User, UserAdmin)
