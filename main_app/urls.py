from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.About.as_view(), name='about'),
  path('journals/', views.JournalList.as_view(), name='public'),
  path('memory/<int:pk>/', views.MemoryDetail.as_view(), name='memory_detail'),
  path('journals/new/', views.JournalCreate.as_view(), name='journal_create'),
]