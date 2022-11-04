from django.contrib import admin
from .models import *
# Register your models here.


@admin.action(description='Register selected users')
def register_users(modeladmin, request, queryset):
    queryset.update(registered=True)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'UUID', 'registered',)
    actions = [register_users]

    def UUID(self, obj):
        return obj.uuid.hex


admin.site.register(Author, AuthorAdmin)
