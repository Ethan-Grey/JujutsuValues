from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Item, ValueChangeRequest, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "item_type",
        "rarity",
        "value",
        "trend",
        "demand",
        "featured",
    )
    list_filter = (
        "category",
        "item_type",
        "rarity",
        "trend",
        "is_limited",
        "featured",
    )
    search_fields = ("name", "notes", "obtained_from")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-featured", "-value")


@admin.register(ValueChangeRequest)
class ValueChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "requested_by",
        "current_value",
        "requested_value",
        "status",
        "created_at",
        "reviewed_by",
    )
    list_filter = ("status", "created_at", "reviewed_at")
    search_fields = ("item__name", "requested_by__username", "reason")
    readonly_fields = ("created_at", "reviewed_at")
    fieldsets = (
        ("Request Details", {
            "fields": ("item", "requested_by", "current_value", "requested_value", "reason")
        }),
        ("Review", {
            "fields": ("status", "reviewed_by", "review_notes", "reviewed_at")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    def save_model(self, request, obj, form, change):
        # If status is being changed and reviewed_by is not set, set it to current user
        if change and "status" in form.changed_data and not obj.reviewed_by:
            if request.user.is_superuser:
                obj.reviewed_by = request.user
                from django.utils import timezone
                obj.reviewed_at = timezone.now()
                
                # If approved, update the item value
                if obj.status == ValueChangeRequest.Status.APPROVED:
                    obj.item.value = obj.requested_value
                    obj.item.save()
        super().save_model(request, obj, form, change)


# Custom User Admin - Only superusers can assign groups
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    def get_groups(self, obj):
        """Display groups for a user"""
        groups = obj.groups.all()
        if groups:
            return ', '.join([g.name for g in groups])
        return '-'
    get_groups.short_description = 'Groups'
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Only show groups field to superusers
        if not request.user.is_superuser:
            # Remove groups from fieldsets
            fieldsets = list(fieldsets)
            for i, (name, options) in enumerate(fieldsets):
                if 'groups' in options.get('fields', []):
                    fields = list(options['fields'])
                    fields.remove('groups')
                    fieldsets[i] = (name, {'fields': fields})
        return fieldsets

    def has_change_permission(self, request, obj=None):
        # Only superusers can change users (to assign groups)
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "is_verified", "created_at")
    search_fields = ("user__username", "display_name")
    list_filter = ("is_verified", "created_at")
