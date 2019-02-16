from rest_framework.serializers import ModelSerializer

from .models import TodoItem


class TodoItemSerializer(ModelSerializer):

    class Meta:
        model = TodoItem
        fields = ['title', 'completed', 'order']

    def validate(self, attrs):
        order = attrs.pop('order', None)
        # if order was not set in request or if item with given order exists
        if order is None or TodoItem.objects.filter(order=order):
            order = TodoItem.get_next_order_num()
        validated_attrs = {key: value for key, value in attrs.items()}
        validated_attrs['order'] = order
        return validated_attrs
