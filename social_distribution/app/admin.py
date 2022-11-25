from django.contrib import admin
from .models import *
# Register your models here.


@admin.action(description='Register selected users')
def register_users(modeladmin, request, queryset):
    queryset.update(registered=True)


@admin.action(description='Register selected nodes')
def register_nodes(modeladmin, request, queryset):
    queryset.update(registered=True)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'UUID', 'registered',)
    actions = [register_users]

    def UUID(self, obj):
        return obj.uuid.hex


class RemoteNodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'UUID', 'base_url', 'registered',)
    actions = [register_nodes]

    def UUID(self, obj):
        return obj.uuid.hex


class InboxItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def title(self, obj):
        if (url_is_local(obj.from_author_url)):
            from_author = Author.objects.get(
                uuid=obj.from_author_url.split("/")[-1])
            obj.from_author_url = f"{from_author.user.username} ({obj.from_author_url})"

        return f"{obj.type}: {obj.from_author_url} -> {obj.author.user.username}"


class FollowAdmin(admin.ModelAdmin):
    list_display = ('title', 'accepted')

    def title(self, obj):
        if (url_is_local(obj.target_url)):
            from_author = Author.objects.get(
                uuid=obj.target_url.split("/")[-1])
            obj.target_url = f"{from_author.user.username} ({obj.target_url})"

        return f"{obj.target_url} -> {obj.author.user.username}"


admin.site.register(Author, AuthorAdmin)
admin.site.register(RemoteNode, RemoteNodeAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(InboxItem, InboxItemAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment)
