from rest_framework.permissions import BasePermission
from products.models import Product

class ProductAccessPermission(BasePermission):
    """
    Custom permission: Only creators of products can edit, others can read.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if not request.user.is_authenticated or not request.user.is_seller:
            return False
        if request.method == 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if not request.user.is_authenticated or not request.user.is_seller:
            return False
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.created_by != request.user:
                return False
            return True
        return False
    
class ProductImageAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method == 'POST':
            related_product = Product.objects.filter(active=True).get(id=request.data['product'])
            if related_product.created_by == request.user:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if obj.product.created_by != request.user:
            return False
        return True
    
class ReviewAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user.is_authenticated and request.method == 'POST':
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user == obj.user:
            return True
        return False
    
class DiscountAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method == 'POST':
            if not request.user.is_seller:
                return False
            product_ids = request.data['products']
            products = Product.objects.filter(active=True)
            for product_id in product_ids:
                product = products.get(id=product_id)
                if product.created_by != request.user:
                    return False
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method == ['PUT', 'PATCH']:
            if not request.user.is_seller or obj.seller != request.user:
                return False
            if request.data.get('products'):
                product_ids = request.data['products']
                products = Product.objects.filter(active=True)
                for product_id in product_ids:
                    product = products.get(id=product_id)
                    if product.created_by != request.user:
                        return False
            if request.data.get('seller'):
                if request.data.get('seller') != request.user.id:
                    return False
            return True
        if request.method == 'DELETE':
            if obj.user == request.user:
                return True
        return False