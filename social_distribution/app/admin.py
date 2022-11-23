from django.contrib import admin
from .models import *
# Register your models here.


@admin.action(description='Register selected users')
def register_users(modeladmin, request, queryset):
    queryset.update(registered=True)


@admin.action(description='Register selected nodes')
def register_nodes(modeladmin, request, queryset):
    queryset.update(is_remote_node=True)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'UUID', 'registered', 'is_remote_node',)
    actions = [register_users, register_nodes]

    def UUID(self, obj):
        return obj.uuid.hex


class InboxItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def title(self, obj):
        return f"{obj.type} from {obj.from_author_url} to {obj.author.username}"


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(InboxItem, InboxItemAdmin)
admin.site.register(Follow)
admin.site.register(Comment)
