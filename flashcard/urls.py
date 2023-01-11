from django.urls import path
from flashcard import views

urlpatterns = [
	path('cards/', views.CardListView.as_view(), name='card-list'),
	path('cards/<int:pk>/', views.CardDetailView.as_view(), name='card-detail'),
]