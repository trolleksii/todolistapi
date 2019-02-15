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
