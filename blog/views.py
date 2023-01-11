from rest_framework.views import APIView
from blog.models import Category, Post, Comment
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status


class CategoryListView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request, format=None):
        snippets = Category.objects.all()
        filtered_qs = self.filter_queryset(snippets)
        serializer = CategorySerializer(filtered_qs, many=True)
        return Response(serializer.data)


class PostListView(APIView):

    def get(self, request, categories_pk):
        post = Post.objects.filter(categories=categories_pk)

        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request, categories_pk):
        serializer = PostSerializer(data=request.data, context={'request': request, 'categories_pk': categories_pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateComment(APIView):
    serializer_class = CommentSerializer

    def get(self, request, format=None):
        snippets = Comment.objects.all()
        serializer = CommentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
