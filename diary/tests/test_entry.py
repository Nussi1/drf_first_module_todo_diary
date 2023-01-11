from rest_framework.reverse import reverse
from diary.models import Entry
from diary.serializers import EntrySerializer
import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.parsers import MultiPartParser, FormParser
from time import perf_counter

client = APIClient()
response_time = .1


class GetAllEntryTest(TestCase):

    def setUp(self):
        Entry.objects.create(title='diary', content='my diary')
        Entry.objects.create(title='diary2', content='my diary2')
        Entry.objects.create(title='diary3', content='my diary3')
        Entry.objects.create(title='diary4', content='my diary4')
        self.response_time = .1

    def test_get_all_entries(self):
        end = perf_counter()
        response = self.client.get(reverse('entry-list'))
        start = perf_counter()
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleEntryTest(TestCase):

    def setUp(self):
        self.diary1 = Entry.objects.create(title='diary', content='my diary')
        self.diary2 = Entry.objects.create(title='diary2', content='my diary2')
        self.response_time = .1

    def test_get_valid_single_entry(self):
        end = perf_counter()
        response = self.client.get(
            reverse('entry-detail', kwargs={'pk': self.diary1.pk}))
        start = perf_counter()
        entry = Entry.objects.get(pk=self.diary1.pk)
        serializer = EntrySerializer(entry)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_entry(self):
        end = perf_counter()
        response = self.client.get(
            reverse('entry-detail', kwargs={'pk': 30}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewToDoEntryTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'title': 'diary1',
            'content': 'my diary'
        }
        self.invalid_payload = {
            'title': '',
            'content': 'my diary2'
        }
        self.response_time = .1

    def test_create_valid_entry(self):
        end = perf_counter()
        url = reverse('entry-list')
        start = perf_counter()
        request = self.client.post(url, data=self.valid_payload)
        entry = Entry.objects.first()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(entry.content, 'diary1')
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_entry(self):
        end = perf_counter()
        response = client.post(
            reverse('entry-list'),
            data=self.invalid_payload,
            content_type='application/json'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleEntryTest(TestCase):
    parser_classes = (MultiPartParser, FormParser,)

    def setUp(self):
        self.diary1 = Entry.objects.create(title='Diary updated')
        self.diary2 = Entry.objects.create(title='Diary update2')
        self.valid_payload = {
            'title': 'diary1',
            'content': 'my diary'
        }
        self.invalid_payload = {
            'title': '',
            'content': 'my diary'
        }
        self.response_time = .1

    def test_valid_update_entry(self):
        end = perf_counter()
        response = client.put(
            reverse('entry-detail', kwargs={'pk': self.diary1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_entry(self):
        end = perf_counter()
        response = client.put(
            reverse('entry-detail', kwargs={'pk': self.diary1.pk}),
            data=self.invalid_payload,
            content_type='application/json'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleEntryTest(TestCase):

    def setUp(self):
        self.diary1 = Entry.objects.create(title='diary1')
        self.diary2 = Entry.objects.create(title='diary2')
        self.response_time = .1

    def test_valid_delete_entry(self):
        end = perf_counter()
        response = client.delete(
            reverse('entry-detail', kwargs={'pk': self.diary1.pk}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_entry(self):
        end = perf_counter()
        response = client.delete(
            reverse('entry-detail', kwargs={'pk': 30}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
