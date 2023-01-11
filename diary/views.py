from .models import Entry
from .serializers import EntrySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EntryListView(APIView):

    def get(self, request, format=None):
        diaries = Entry.objects.all()
        serializer = EntrySerializer(diaries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntryDetailView(APIView):

    def get_object(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        entries = self.get_object(pk)
        serializer = EntrySerializer(entries)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        entries = self.get_object(pk)
        serializer = EntrySerializer(entries, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
