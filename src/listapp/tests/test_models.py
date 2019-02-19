from django.core.exceptions import ValidationError
from django.test import LiveServerTestCase

from ..models import TodoItem


class TodoItemTests(LiveServerTestCase):
    """Test TodoItem model"""

    def setUp(self):
        data = {
            "title": "The very first item in the list"
        }
        self.todo_item = TodoItem(**data)
        self.todo_item.full_clean()
        self.todo_item.save()

    def test_cant_create_item_without_title(self):
        data = {}
        item = TodoItem(**data)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_todos_are_created_with_proper_defaults(self):
        self.assertIsNone(self.todo_item.order)
        self.assertFalse(self.todo_item.completed)

    def test_get_next_order_num_first_item(self):
        self.assertEqual(TodoItem.get_next_order_num(), 1)

    def test_get_next_order_num_second_item(self):
        item = TodoItem.objects.create(
            title="Finish the app",
            order=2
        )
        self.assertEqual(TodoItem.get_next_order_num(), 3)
