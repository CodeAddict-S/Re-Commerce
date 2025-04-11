from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework.response import Response

# Create your views here.
class BaseModelViewSet(ModelViewSet):
    """
    this viewset is for adding 'created_by', 'updated_by', 'created_at', 'updated_at' fields before creating or updating
    """
    def list(self, request):
        limit = request.query_params.get('limit')
        queryset = self.get_queryset()
        if limit:
            queryset = queryset[:int(limit)]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({
            'created_by':request.user,
            'created_at':timezone.now(),
            'updated_by':request.user,
            'updated_at':timezone.now()
        })
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)  

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        data.update({
            'updated_by':request.user,
            'updated_at':timezone.now()
        })
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)  