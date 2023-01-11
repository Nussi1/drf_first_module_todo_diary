from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    technology = serializers.CharField(read_only=True)
    image = serializers.ImageField()
