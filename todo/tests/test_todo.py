from rest_framework.reverse import reverse
from todo.models import ToDoList, ToDoItem
from todo.serializers import ToDoListSerializer, ToDoItemSerializer
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.parsers import MultiPartParser, FormParser
from time import perf_counter

client = APIClient()
response_time = .1


class GetAllToDoTest(TestCase):

    def setUp(self):
        ToDoList.objects.create(title='Dance')
        ToDoList.objects.create(title='Buy')
        ToDoList.objects.create(title='Cook')
        ToDoList.objects.create(title='Learn')
        self.response_time = .1

    def test_get_all_todos(self):
        end = perf_counter()
        response = self.client.get(reverse('get_post_todolist'))
        start = perf_counter()
        todos = ToDoList.objects.all()
        serializer = ToDoListSerializer(todos, many=True)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleToDoTest(TestCase):

    def setUp(self):
        self.dance = ToDoList.objects.create(title='Dance')
        self.buy = ToDoList.objects.create(title='Buy')
        self.cook = ToDoList.objects.create(title='Cook')
        self.learn = ToDoList.objects.create(title='Learn')
        self.response_time = .1

    def test_get_valid_single_todo(self):
        end = perf_counter()
        response = self.client.get(
            reverse('get_delete_update_todo', kwargs={'pk': self.dance.pk}))
        start = perf_counter()
        todo = ToDoList.objects.get(pk=self.dance.pk)
        serializer = ToDoListSerializer(todo)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_todo(self):
        end = perf_counter()
        response = self.client.get(
            reverse('get_delete_update_todo', kwargs={'pk': 30}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewToDoTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'title': 'Buy'
        }
        self.invalid_payload = {
            'title': ''
        }
        self.response_time = .1

    def test_create_valid_todolist(self):
        end = perf_counter()
        url = reverse('get_post_todolist')
        start = perf_counter()
        request = self.client.post(url, data=self.valid_payload)
        todolist = ToDoList.objects.first()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(todolist.title, 'Buy')
        self.assertEqual(ToDoList.objects.count(), 1)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_todolist(self):
        end = perf_counter()
        response = client.post(
            reverse('get_post_todolist'),
            data=self.invalid_payload,
            content_type='multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleToDoTest(TestCase):
    parser_classes = (MultiPartParser, FormParser,)

    def setUp(self):
        self.dance = ToDoList.objects.create(title='Dance')
        self.buy = ToDoList.objects.create(title='Buy')
        self.valid_payload = {
            'title': 'Buy',
        }
        self.invalid_payload = {
            'title': '',
        }
        self.response_time = .1

    def test_valid_update_todolist(self):
        end = perf_counter()
        response = client.put(
            reverse('get_delete_update_todo', kwargs={'pk': self.buy.pk}),
            data=self.valid_payload,
            content_type='multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_todolist(self):
        end = perf_counter()
        response = client.put(
            reverse('get_delete_update_todo', kwargs={'pk': self.buy.pk}),
            data=self.invalid_payload,
            content_type='multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleToDoListTest(TestCase):

    def setUp(self):
        self.dance = ToDoList.objects.create(title='Dance')
        self.buy = ToDoList.objects.create(title='Buy')
        self.response_time = .1

    def test_valid_delete_todolist(self):
        end = perf_counter()
        response = client.delete(
            reverse('get_delete_update_todo', kwargs={'pk': self.buy.pk}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_todolist(self):
        end = perf_counter()
        response = client.delete(
            reverse('get_delete_update_todo', kwargs={'pk': 30}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllToDoItemTest(TestCase):
    url = "/dotoitem/1"

    def setUp(self):

        self.list_ = ToDoList.objects.create(title='read')
        self.item = ToDoItem.objects.create(title='Dance', description='dancing', created_date='2022-12-14', due_date='2022-12-30', todo_list_id=self.list_.id)
        ToDoItem.objects.create(title='Buy', description='purchasing', created_date='2022-12-14', due_date='2022-12-30', todo_list_id=self.list_.id)
        ToDoItem.objects.create(title='Cook', description='cake', due_date='2022-12-30', todo_list_id=self.list_.id)
        ToDoItem.objects.create(title='Learn', description='read', due_date='2022-12-30', todo_list_id=self.list_.id)
        self.response_time = .1

    def test_get_all_items(self):
        end = perf_counter()
        response = self.client.get(reverse('get_post_todoitem'), kwargs={'todolist_pk': self.list_.pk, 'todoitem_pk': self.item.pk})
        print(response.data)
        start = perf_counter()
        todos = ToDoItem.objects.all()
        serializer = ToDoItemSerializer(todos, many=True)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleToDoItemTest(TestCase):

    def setUp(self):
        self.list_ = ToDoList.objects.create(title='read')
        self.dance = ToDoItem.objects.create(title='Dance', description='dancing', due_date='2022-12-30', todo_list_id=self.list_.id)
        self.buy = ToDoItem.objects.create(title='Buy', description='purchasing', due_date='2022-12-30', todo_list_id=self.list_.id)
        self.cook = ToDoItem.objects.create(title='Cook', description='cake', due_date='2022-12-30', todo_list_id=self.list_.id)
        self.learn = ToDoItem.objects.create(title='Learn', description='read', due_date='2022-12-30', todo_list_id=self.list_.id)
        self.response_time = .1

    def test_get_valid_single_item(self):
        end = perf_counter()
        response = self.client.get(
            reverse('get_delete_update_todoitem', kwargs={'pk': self.dance.pk}))
        start = perf_counter()
        todo = ToDoItem.objects.get(pk=self.dance.pk)
        serializer = ToDoItemSerializer(todo)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_item(self):
        end = perf_counter()
        response = self.client.get(
            reverse('get_delete_update_todoitem', kwargs={'pk': 30}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
