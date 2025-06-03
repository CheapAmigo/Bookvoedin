from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BookCard

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'phone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('full_name', 'phone', 'email')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

class BookCardAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'user', 'book_type', 'status')
    list_filter = ('status', 'book_type')
    search_fields = ('author', 'title', 'user__username')

admin.site.register(User, CustomUserAdmin)
admin.site.register(BookCard, BookCardAdmin)