from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import TodoItemSerializer
from .models import TodoItem


class TodoItemViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    serializer_class = TodoItemSerializer
    queryset = TodoItem.objects.all()
    lookup_field = 'pk'

    @list_route(methods=['DELETE'], permission_classes=[AllowAny], url_name='flush')
    def flush(self, request):
        TodoItem.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
