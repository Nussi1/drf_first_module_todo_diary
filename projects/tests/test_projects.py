from rest_framework.reverse import reverse
from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from time import perf_counter

client = APIClient()
response_time = .1


class GetAllToDoTest(TestCase):

    def setUp(self):
        Project.objects.create(title='Proj 1', description='desk', technology='tech', image='im.jpg')
        Project.objects.create(title='Proj 2', description='desk', technology='tech', image='im.jpg')
        Project.objects.create(title='Proj 3', description='desk', technology='tech', image='im.jpg')
        Project.objects.create(title='proj 4', description='desk', technology='tech', image='im.jpg')
        self.response_time = .1

    def test_get_all_todos(self):
        end = perf_counter()
        response = self.client.get(reverse('project-list'))
        start = perf_counter()
        proj = Project.objects.all()
        serializer = ProjectSerializer(proj, many=True)
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)