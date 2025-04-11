from django.urls import path, include
from products.views import (
    ProductViewSet,
    ProductImageViewSet,
    CategoryViewSet,
    ProductReviewViewSet,
    DiscountEventViewSet,
    CategoryGroupViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('product-images', ProductImageViewSet, basename='product_image')
router.register('categories', CategoryViewSet, basename='category')
router.register('product-reviews', ProductReviewViewSet, basename='product_reviews')
router.register('discount-events', DiscountEventViewSet, basename='disocunt_event')
router.register('category-groups', CategoryGroupViewSet, basename='category_groups')

urlpatterns = [
    path('', include(router.urls))
]