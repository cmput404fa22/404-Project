from rest_framework import permissions


class IsRemoteNode(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.author.is_remote_node:
            return True
        return False
