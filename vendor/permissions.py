from rest_framework.permissions import BasePermission

class IsCreationOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create' and request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated