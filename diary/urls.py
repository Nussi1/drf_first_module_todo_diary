from django.urls import path
from diary import views

urlpatterns = [
	path('entry/', views.EntryListView.as_view(), name='entry-list'),
	path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry-detail'),
]