from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.About.as_view(), name='about'),
  path('public/', views.PublicList.as_view(), name='public'),
  path('accounts/register/', views.RegisterView.as_view(), name='register'),
  path('memory/<int:pk>/', views.MemoryDetail.as_view(), name='memory_detail'),
  path('journals/new/', views.JournalCreate.as_view(), name='journal_create'),
  path('memory/new/', views.MemoryCreate.as_view(), name='memory_create'),
  path('memory/<int:pk>/update/', views.MemoryUpdate.as_view(), name='memory_update'),
  path('journals/<int:pk>/', views.JournalDetail.as_view(), name='journal_detail'),
  path('memory/<int:pk>/delete/', views.MemoryDelete.as_view(), name='memory_delete'),
  path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journal_delete'),
  path('journals/', views.JournalList.as_view(), name='journal_list'),
  path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journal_update'),
  path('albums/', views.AlbumList.as_view(), name='albums_list'),
  path('albums/<int:pk>/', views.AlbumDetail.as_view(), name='album_detail'),
  path('albums/new/', views.AlbumCreate.as_view(), name='album_create'),
  path('albums/<int:pk>/update/', views.AlbumUpdate.as_view(), name='album_update'),
  path('albums/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album_delete'),
  path('photo/<int:pk>/', views.PhotoDetail.as_view(), name='photo_detail'),
  path('photo/new/', views.PhotoCreate.as_view(), name='photo_create'),
  path('photo/<int:pk>/update/', views.PhotoUpdate.as_view(), name='photo_update'),
  path('photo/<int:pk>/delete/', views.PhotoDelete.as_view(), name='photo_delete'),
]