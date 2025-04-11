from orders.serializers import (
    OrderSerializer,
    OrderItemSerializer
)
from orders.models import (
    Order,
    OrderItem
)
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions

# Create your views here.
class OrderViewSet(viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.mixins.UpdateModelMixin,
                   viewsets.mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = self.get_serializer(request.user.orders, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        data = {
            "user": request.user.id,
            "seller": request.data['seller'],
            "status": 'pending'
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for order_item in request.data['order_items']:
            serializer = self.get_serializer(data={'product':order_item['id'],'amount':order_item['amount']})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def update(self, request, pk, partial):
        instance = self.get_object()
        if instance.seller != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data.update({
            "user": instance.user.id,
            "seller": instance.seller.id,
            "status": request.data['status']
        })
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    
    def destroy(self, request, pk):
        instance = self.get_object()
        if instance.seller == request.user or instance.user == request.user:
            instance.status = 'cancelled'
            instance.save()
            return Response({'detail':'order cancelled'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
        
class OrderItemViewSet(viewsets.GenericViewSet,
                       viewsets.mixins.ListModelMixin):
    queryset = OrderItem.objects.filter(active=True)
    serializer_class = OrderItemSerializer

    def list(self, request):
        if request.user.is_authenticated:
            order_items_tied_to_user = self.get_queryset().filter(order__in=request.user.orders.all())
            serializer = self.get_serializer(order_items_tied_to_user, many=True)
            return Response(serializer.data)
        # user not authenticated
        return Response(status=status.HTTP_401_UNAUTHORIZED)