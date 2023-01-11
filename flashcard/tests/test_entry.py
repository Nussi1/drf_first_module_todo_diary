from rest_framework.reverse import reverse
from flashcard.models import Card
from flashcard.serializers import CardSerializer
import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.parsers import MultiPartParser, FormParser
from time import perf_counter

client = APIClient()
response_time = .1


class GetAllCardTest(TestCase):

    def setUp(self):
        Card.objects.create(question='are you here?', answer='yes')
        Card.objects.create(question='are you here2?', answer='no')
        Card.objects.create(question='are you here3?', answer='yes')
        Card.objects.create(question='are you here4?', answer='no')
        self.response_time = .1

    def test_get_all_cards(self):
        end = perf_counter()
        response = self.client.get(reverse('card-list'))
        start = perf_counter()
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCardTest(TestCase):

    def setUp(self):
        self.card1 = Card.objects.create(question='are you here?', answer='yes')
        self.card2 = Card.objects.create(question='are you here2?', answer='no')
        self.response_time = .1

    def test_get_valid_single_card(self):
        end = perf_counter()
        response = self.client.get(
            reverse('card-detail', kwargs={'pk': self.card1.pk}))
        start = perf_counter()
        entry = Card.objects.get(pk=self.card1.pk)
        serializer = CardSerializer(entry)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_card(self):
        response = self.client.get(
            reverse('card-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCardTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'question': 'you?',
            'answer': 'yes'
        }
        self.invalid_payload = {
            'question': '',
            'answer': 'yes'
        }
        self.response_time = .1

    def test_create_valid_card(self):
        end = perf_counter()
        url = reverse('card-list')
        start = perf_counter()
        request = self.client.post(url, data=self.valid_payload)
        card = Card.objects.first()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(card.question, 'you?')
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_card(self):
        end = perf_counter()
        response = client.post(
            reverse('card-list'),
            data=self.invalid_payload,
            content_type='application/json'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCardTest(TestCase):
    parser_classes = (MultiPartParser, FormParser,)

    def setUp(self):
        self.card1 = Card.objects.create(question='hi?')
        self.card2 = Card.objects.create(question='you?')
        self.valid_payload = {
            'question': 'you?',
            'answer': 'yes'
        }
        self.invalid_payload = {
            'question': '',
            'answer': 'yes'
        }
        self.response_time = .1

    def test_valid_update_card(self):
        end = perf_counter()
        response = client.put(
            reverse('card-detail', kwargs={'pk': self.card1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        start = perf_counter()
        print(response.data)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_card(self):
        end = perf_counter()
        response = client.put(
            reverse('card-detail', kwargs={'pk': self.card1.pk}),
            data=self.invalid_payload,
            content_type='application/json'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCardTest(TestCase):

    def setUp(self):
        self.card1 = Card.objects.create(question='are you here?', answer='yes')
        self.card2 = Card.objects.create(question='are you here2?', answer='no')
        self.response_time = .1

    def test_valid_delete_card(self):
        end = perf_counter()
        response = client.delete(
            reverse('card-detail', kwargs={'pk': self.card1.pk}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_card(self):
        end = perf_counter()
        response = client.delete(
            reverse('card-detail', kwargs={'pk': 30}))
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
