from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_cents", "is_available", "created_at")
    list_filter = ("is_available",)
    search_fields = ("name",)

# Register your models here.
