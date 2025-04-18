from django.contrib import admin
from .models import Profile
from .models import Role, CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(Profile)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {'fields': ('role',)}),
    )

admin.site.register(Role)
admin.site.register(CustomUser, CustomUserAdmin)