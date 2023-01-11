from django.urls import path
from todo import views
from rest_framework import permissions




urlpatterns = [
    path('todolist/', views.ToDoListList.as_view(), name='get_post_todolist'),
    path('todolist/<int:pk>/', views.ToDoListDetail.as_view(), name='get_delete_update_todo'),
    path('todoitem/<int:todolist_pk>/', views.ToDoItemList.as_view(), name='get_post_todoitem'),
    path('todoitem/<int:todolist_pk>/<int:todoitem_pk>/', views.ToDoItemDetail.as_view(), name='get_delete_update_todoitem'),

]