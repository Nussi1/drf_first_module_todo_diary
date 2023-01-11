from django.http import Http404
from rest_framework.views import APIView
from projects.models import Project
from .serializers import ProjectSerializer
from rest_framework.response import Response


class ProjectListView(APIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, format=None):
        snippets = Project.objects.all()
        serializer = ProjectSerializer(snippets, many=True)
        return Response(serializer.data)


class ProjectDetail(APIView):

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProjectSerializer(snippet)
        return Response(serializer.data)
