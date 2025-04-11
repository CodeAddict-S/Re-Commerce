from django.urls import path, include
from users.views import UserViewSet, user_verify, user_reset_password, MerchantViewSet, MerchantApplicationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'merchants', MerchantViewSet)
router.register(r'merchant-applications', MerchantApplicationViewSet)
router.register(r'', UserViewSet)

urlpatterns = [
    path('verify/<int:pk>', user_verify),
    path('reset-password/<int:pk>', user_reset_password),
    path('', include(router.urls)),
]