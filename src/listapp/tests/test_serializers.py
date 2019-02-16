from django.test import LiveServerTestCase

from ..models import TodoItem
from ..serializers import TodoItemSerializer


class TodoItemSerializerTests(LiveServerTestCase):
    """Test TodoItem serializer"""
    def test_can_serialize_data(self):
        todo_item = TodoItem(
            title='task 1'
        )
        serializer = TodoItemSerializer(todo_item)
        self.assertEqual(
            serializer.data,
            {'title': 'task 1', 'order': None, 'completed': False}
        )

    def test_deserialize_saves_new_todo_item(self):
        data = {
            'title': 'task 2',
            'order': 2
        }
        serializer = TodoItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        todoitem = TodoItem.objects.first()
        self.assertEqual(todoitem.title, data['title'])
        self.assertEqual(todoitem.order, data['order'])
