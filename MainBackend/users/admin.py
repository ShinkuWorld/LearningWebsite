from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'email', 'phone')
    list_filter = ('user_type',)
    search_fields = ('username', 'email', 'phone', 'student_id', 'teacher_id')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('用户类型', {'fields': ('user_type', 'student_id', 'teacher_id')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
