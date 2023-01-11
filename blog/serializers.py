from rest_framework import serializers
from blog.models import *


class CommentSerializer(serializers.Serializer):
    author = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())
    body = serializers.CharField(max_length=500)
    created_on = serializers.DateTimeField(read_only=True)
    post = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['author', 'body', 'created_on', 'post']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post_pk = validated_data.pop('post')
        return Comment.objects.create(**validated_data, post_id=post_pk)

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    last_modified = serializers.DateTimeField(read_only=True)
    categories = serializers.CharField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data, categories_id=self.context['categories_pk'])


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
