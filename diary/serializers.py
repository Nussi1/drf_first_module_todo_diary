from rest_framework import serializers
from .models import Entry


class EntrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=300)
    date_created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Entry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        return instance
