from django.test import LiveServerTestCase
from django.shortcuts import reverse
from django.test import LiveServerTestCase

from rest_framework import status

from ..models import TodoItem
from ..serializers import TodoItemSerializer


class TodoItemViewsetTests(LiveServerTestCase):
    """Test TodoItem viewset"""
    def setUp(self):
        self.item_count = 10
        for x in range(self.item_count):
            TodoItem.objects.create(title=f'Todo Item #{x + 1}')

    def test_can_create_todo_item(self):
        response = self.client.post(
            reverse('listapp:todoitems-list'),
            data={'title': 'Write some more tests'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        qset = TodoItem.objects.filter(title='Write some more tests')
        self.assertEqual(len(qset), 1)

    def test_can_list_todo_items(self):
        response = self.client.get(
            reverse('listapp:todoitems-list'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.item_count)

    def test_can_list_todo_items_with_pagination(self):
        page = 5
        response = self.client.get(
            reverse('listapp:todoitems-list') + f'?limit={page}&offset=0',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.item_count)
        self.assertIsNone(response.data['previous'])
        self.assertRegex(response.data['next'], r'limit={0}&offset={0}'.format(page))
        self.assertEqual(len(response.data['results']), page)

    def test_can_query_individual_todo_item(self):
        todo_item = TodoItem.objects.last()
        response = self.client.get(
            reverse('listapp:todoitems-detail', kwargs={'pk': todo_item.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], todo_item.title)

    def test_can_update_todo_item(self):
        todo_item = TodoItem.objects.first()
        response = self.client.patch(
            reverse('listapp:todoitems-detail', kwargs={'pk': todo_item.pk}),
            data={'completed': True},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo_item.refresh_from_db()
        self.assertTrue(todo_item.completed)

    def test_can_delete_single_todo_item(self):
        todo_item = TodoItem.objects.first()
        response = self.client.delete(
            reverse('listapp:todoitems-detail', kwargs={'pk': todo_item.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(TodoItem.DoesNotExist):
            todo_item.refresh_from_db()

    def test_can_delete_all_items(self):
        response = self.client.delete(
            reverse('listapp:todoitems-flush'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        all_items = TodoItem.objects.all()
        self.assertEqual(len(all_items), 0)
