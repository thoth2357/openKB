from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kb.models import Article, CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
    
    
admin.site.register(Article)
admin.site.register(CustomUser, UserAdmin)
