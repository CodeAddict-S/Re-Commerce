from rest_framework import viewsets
from products.models import (
    Product,
    ProductImage,
    Category,
    ProductReview,
    DiscountEvent,
    CategoryGroup
)
from products.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    CategorySerializer,
    ProductReviewSerializer,
    DiscountEventSerializer,
    CategoryGroupSerializer
)
from products.permissions import (
    ProductAccessPermission,
    ProductImageAccessPermission,
    ReviewAccessPermission,
    DiscountAccessPermission
)
from utils.views import BaseModelViewSet

# Create your views here.
class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductAccessPermission]
    
class ProductImageViewSet(BaseModelViewSet):
    queryset = ProductImage.objects.filter(active=True)
    serializer_class = ProductImageSerializer
    permission_classes = [ProductImageAccessPermission]
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

class CategoryGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryGroup.objects.filter(active=True)
    serializer_class = CategoryGroupSerializer

class ProductReviewViewSet(BaseModelViewSet):
    queryset = ProductReview.objects.filter(active=True)
    serializer_class = ProductReviewSerializer
    permission_classes = [ReviewAccessPermission]
    
class DiscountEventViewSet(BaseModelViewSet):
    queryset = DiscountEvent.objects.filter(active=True)
    serializer_class = DiscountEventSerializer
    permission_classes = [DiscountAccessPermission]