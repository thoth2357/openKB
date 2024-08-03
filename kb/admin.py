from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.urls import reverse
from kb.models import Article, CustomUser, Settings, ArticleSettings, DisplaySettings, StyleSettings

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
    
class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Disable add permission if an instance already exists
        count = self.model.objects.count()
        if count >= 1:
            return False
        return True

    def changelist_view(self, request, extra_context=None):
        # Redirect to the change view if an instance already exists
        try:
            obj = self.model.objects.get()
            return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=[obj.pk]))
        except self.model.DoesNotExist:
            return super().changelist_view(request, extra_context)

admin.site.register(Article)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Settings, SingletonAdmin)
admin.site.register(ArticleSettings, SingletonAdmin)
admin.site.register(DisplaySettings, SingletonAdmin)
admin.site.register(StyleSettings, SingletonAdmin)