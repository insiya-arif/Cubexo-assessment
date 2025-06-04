from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, ReadingList, OTP

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_verified', 'is_staff', 'is_active'),
        }),
    )

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_at')
    search_fields = ('user__email', 'book__title')
    list_filter = ('added_at',)

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'code', 'created_at', 'expires_at')
    search_fields = ('user_email', 'code')
    list_filter = ('created_at', 'expires_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(ReadingList, ReadingListAdmin)
admin.site.register(OTP, OTPAdmin)