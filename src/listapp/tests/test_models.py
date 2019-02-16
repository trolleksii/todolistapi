from django.core.exceptions import ValidationError
from django.test import LiveServerTestCase

from ..models import TodoItem


class TodoItemTests(LiveServerTestCase):
    """Test TodoItem model"""
    def test_can_create_item_with_title_set(self):
        data = {
            "title": "The very first item in the list"
        }
        item = TodoItem(**data)
        item.full_clean()
        item.save()
        self.assertEqual(item, TodoItem.objects.first())

    def test_cant_create_item_without_title(self):
        data = {}
        item = TodoItem(**data)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_get_next_order_num_with_empty_db(self):
        self.assertEqual(TodoItem.get_next_order_num(), 1)

    def test_get_next_order_num_if_not_first(self):
        item = TodoItem.objects.create(title="Finish the app", order=2)
        self.assertEqual(TodoItem.get_next_order_num(), 3)
