from rest_framework.reverse import reverse
from blog.models import Category, Post, Comment
from blog.serializers import CategorySerializer, PostSerializer, CommentSerializer
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from time import perf_counter

client = APIClient()
response_time = .1


class GetAllCategoryTest(TestCase):

    def setUp(self):
        Category.objects.create(name='new')
        self.response_time = .1

    def test_get_all_todos(self):
        end = perf_counter()
        response = self.client.get(reverse('category-list'))
        start = perf_counter()
        cat = Category.objects.all()
        serializer = CategorySerializer(cat, many=True)

        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPosts(TestCase):

    def test_blog_has_a_category(self):
        blog = Post.objects.create(title="new post")
        cat1 = Category.objects.create(name="Philip")
        cat2 = Category.objects.create(name="Juliana")
        blog.categories.set([cat1.pk, cat2.pk])
        self.assertEqual(blog.categories.count(), 2)


class CreateNewPostTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Python')

        self.valid_payload = {
            'title': 'Buy',
            'body': 'hjgj',
            'categories': self.category.pk
        }
        self.invalid_payload = {
            'title': '',
            'body': 'hjgj',
            'categories': self.category.pk
        }
        self.response_time = .1

    def test_create_valid_post(self):
        end = perf_counter()
        url = reverse('post-list', kwargs={'categories_id': self.category.pk})
        start = perf_counter()

        request = self.client.post(url, data=self.valid_payload)
        posts = Post.objects.first()

        self.assertLess(end - start, self.response_time)
        self.assertEqual(posts.title, 'Buy')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self,):
        end = perf_counter()
        response = client.post(
            reverse('post-list', kwargs={'categories_id': self.category.pk}),
            data=self.invalid_payload,
            content_type='application/json'
        )
        start = perf_counter()

        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewCommentTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='post')

        self.valid_payload = {
            'autor': 'Buy',
            'body': 'hjgj',
            'post': self.post.pk
        }
        self.invalid_payload = {
            'author': '',
            'body': 'hjgj',
            'post': self.post.pk
        }
        self.response_time = .1

    def test_create_valid_comment(self):
        end = perf_counter()
        url = reverse('comments')
        start = perf_counter()
        request = self.client.post(url, data=self.valid_payload)
        comments = Comment.objects.first()

        self.assertLess(end - start, self.response_time)
        self.assertEqual(comments.author, 'AnonymousUser')
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_comment(self):
        end = perf_counter()
        response = client.post(
            reverse('comments'),
            data=self.invalid_payload,
            content_type='application/json'
        )
        start = perf_counter()
        self.assertLess(end - start, self.response_time)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
