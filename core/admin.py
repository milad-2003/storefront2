from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Copied this from "BaseUserAdmin" and only added "email", "first_name" and "last_name"
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
    search_fields = ['username__istartswith', 'first_name__istartswith', 'last_name__istartswith']


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
