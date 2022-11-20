from rest_framework import permissions


class IsRemoteNode(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.author.is_remote_node:
            return True
        return False
