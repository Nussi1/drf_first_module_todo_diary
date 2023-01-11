from rest_framework import serializers
from .models import ToDoList, ToDoItem


class ToDoItemSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=300)
    created_date = serializers.DateTimeField()
    due_date = serializers.DateTimeField()
    todo_list = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return ToDoItem.objects.create(**validated_data, todolist_id=self.context['todolist_pk'])

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        return instance


class ToDoListSerializer(serializers.Serializer):
    todo_list = ToDoItemSerializer(many=True, read_only=True)
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)

    def create(self, validated_data):
        ToDoList.objects.create(**validated_data).save()
        return ToDoItem(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


