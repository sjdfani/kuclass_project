from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, EmailCode


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "username", "is_staff", "is_active",)
    list_filter = ("is_superuser", "is_staff", "is_active",)
    fieldsets = (
        ('Personal Information', {
         "fields": ("email", "username", "fullname", "major", "password", "photo")}),
        ("Permissions", {
            "fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2", "is_superuser", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class EmailCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'updated_at')
    search_fields = ('user',)
    ordering = ('-updated_at',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(EmailCode, EmailCodeAdmin)
