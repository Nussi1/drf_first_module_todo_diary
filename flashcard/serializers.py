from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField(max_length=200)
    answer = serializers.CharField(max_length=300)
    box = serializers.IntegerField()
    date_created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.answer = validated_data.get('answer', instance.answer)
        instance.box = validated_data.get('box', instance.box)
        return instance