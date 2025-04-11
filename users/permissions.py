from rest_framework.permissions import BasePermission

class MerchantAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
            return request.user.is_superuser
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
            return request.user.is_superuser
        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user or request.is_superuser
        if request.method == 'DELETE':
            return obj.user == request.user or request.is_superuser
        return False

class MerchantApplicationAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_superuser
        if request.method == 'POST':
            return request.data['user'] == request.user.id
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_superuser
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_superuser
        if request.method == 'DELETE':
            return obj.user == request.user 
        return False