from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'superadmin' or request.user.is_superuser))

class IsEditorOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role in ['superadmin', 'editor'] or request.user.is_staff))

class IsReporterOrAbove(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role in ['superadmin', 'editor', 'reporter'] or request.user.is_staff))

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['superadmin', 'editor'] or request.user.is_superuser:
            return True
        return obj == request.user
