from .models import ToDoList, ToDoItem
from .serializers import ToDoListSerializer, ToDoItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class ToDoListList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        todolists = ToDoList.objects.all()
        serializer = ToDoListSerializer(todolists, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=ToDoListSerializer)
    def post(self, request, format=None):
        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoListDetail(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return ToDoList.objects.get(pk=pk)
        except ToDoList.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        todolist = self.get_object(pk)
        serializer = ToDoListSerializer(todolist)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=ToDoListSerializer)
    def put(self, request, pk, format=None):
        todolist = self.get_object(pk)
        serializer = ToDoListSerializer(todolist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todolist = self.get_object(pk)
        todolist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToDoItemList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, todolist_pk):
        todoitem = ToDoItem.objects.filter(todo_list_id=todolist_pk)
        for item in todoitem:
            self.check_object_permissions(request, item.todo_list)

        serializer = ToDoItemSerializer(todoitem, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=ToDoItemSerializer)
    def post(self, request, todolist_pk):
        serializer = ToDoItemSerializer(data=request.data, context={'request': request, 'todolist_pk': todolist_pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoItemDetail(APIView):
    queryset = ToDoItem.objects.all()
    serializer_class = ToDoItemSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, todolist_pk, todoitem_pk):
        try:
            return ToDoItem.objects.get(todolist_id=todolist_pk, pk=todoitem_pk)
        except ToDoItem.DoesNotExist:
            raise Http404

    def get(self, request, todolist_pk, todoitem_pk):
        item_obj = self.get_object(todolist_pk, todoitem_pk)
        serializer = ToDoItemSerializer(item_obj)

        return Response(serializer.data)

    # @swagger_auto_schema(request_body=ToDoItemSerializer)
    def put(self, request, todolist_pk, todoitem_pk):
        item_obj = self.get_object(todolist_pk, todoitem_pk)
        serializer = ToDoItemSerializer(data=request.data, instance=item_obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(request_body=ToDoItemSerializer)
    def patch(self, request, todolist_pk, todoitem_pk):
        item_obj = self.get_object(todolist_pk, todoitem_pk)
        serializer = ToDoItemSerializer(data=request.data, instance=item_obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todolist_pk, todoitem_pk, format=None):
        object = self.get_object(todolist_pk, todoitem_pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

