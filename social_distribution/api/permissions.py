from rest_framework import permissions


class IsRemoteNode(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or (hasattr(request.user, 'remotenode') and request.user.remotenode.registered):
            return True
        return False
