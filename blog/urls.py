from django.urls import path
from blog import views


urlpatterns = [
	path('category/', views.CategoryListView.as_view(), name='category-list'),
	path('post/<int:categories_pk>/', views.PostListView.as_view(), name='post-list'),
	path('comment/', views.CreateComment.as_view(), name='comments'),
]