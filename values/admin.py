from django.contrib import admin

from .models import Category, Item


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

# Register your models here.
