from django.urls import path
from projects import views


urlpatterns = [
	path('', views.ProjectListView.as_view(), name='project-list'),
	path('<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
]
