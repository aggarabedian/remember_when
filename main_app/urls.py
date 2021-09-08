from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.About.as_view(), name='about'),
  path('journals/', views.JournalList.as_view(), name='journals'),
  path('memory/<int:pk>/', views.MemoryView.as_view(), name='memory'),
]