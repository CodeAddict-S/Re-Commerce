from users.serializers import UserSerializer, MerchantSerializer, MerchantApplicationSerializer
from users.models import User, Merchant, MerchantApplication
from users.permissions import MerchantAccessPermission, MerchantApplicationAccessPermission
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from core import settings
import uuid
from utils.views import BaseModelViewSet

# Create your views here.
class UserViewSet(viewsets.GenericViewSet,
                  viewsets.mixins.ListModelMixin,
                  viewsets.mixins.CreateModelMixin,
                  viewsets.mixins.DestroyModelMixin,
                  viewsets.mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            data = serializer.data
            del data["password"]
            del data["activation_token"]
            del data["id"]
            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def create(self, request):
        new_user_data = User.objects.create_user(email=request.data['email'], password=request.data['password'])
        relative_activation_link = f'/users/verify/{new_user_data.id}?activation_token={new_user_data.activation_token}'
        activation_link = request.build_absolute_uri(relative_activation_link)
        send_mail(
            subject="Verify Your Account (Re-Commerce)",
            message=f"Click the link to activate your account: {activation_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_user_data.email],
        )
        return Response({'detail':'success'}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        instance = self.get_object()
        if request.user == instance:
            instance.active = False
            return Response({"detail":"Successful deletion"})
        return Response({"detail":"unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, pk):
        request.user.activation_token = str(uuid.uuid4())
        request.user.save()
        relative_activation_link = f'/users/reset-password/{request.user.id}?activation_token={request.user.activation_token}&new_password={request.data['password']}'
        activation_link = request.build_absolute_uri(relative_activation_link)
        send_mail(
            subject="Reset your Password (Re-Commerce)",
            message=f"Click the link to reset your password: {activation_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
        )
        return Response({'detail':'success'}, status=status.HTTP_201_CREATED)
    
def user_verify(request, pk):
    user = User.objects.get(id=pk)
    if str(user.activation_token) == request.GET.get('activation_token'):
        user.is_active = True
        user.activation_token = None
        user.save()
        return HttpResponse('successfully verfied your re-commerce account')
    else:
        return HttpResponse('invalid url')
    
def user_reset_password(request, pk):
    user = User.objects.get(id=pk)
    if str(user.activation_token) == request.GET.get('activation_token'):
        user.set_password(request.GET.get('new_password'))
        user.activation_token = None
        user.save()
        return HttpResponse('successfully reset your re-commerce account\'s password')
    else:
        return HttpResponse('invalid url')
    
class MerchantViewSet(BaseModelViewSet):
    queryset = Merchant.objects.filter(active=True)
    serializer_class = MerchantSerializer
    permission_classes = [MerchantAccessPermission]

class MerchantApplicationViewSet(BaseModelViewSet):
    queryset = MerchantApplication.objects.filter(active=True)
    serializer_class = MerchantApplicationSerializer
    permission_classes = [MerchantApplicationAccessPermission]