from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('request.user:', request.user, 'obj.user:', obj.user)
        return obj.user == request.user
