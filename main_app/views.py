from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin


# Imports Models
from .models import Journal, Memory, Album, Photo
from django.contrib.auth.models import User

# Create your views here.

class Home(TemplateView):
  template_name = "home.html"


class About(TemplateView):
  template_name = "about.html"


class PublicList(TemplateView):
  template_name = "memories_public.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["memories"] = Memory.objects.filter(is_public = True)
    return context

@method_decorator(login_required, name='dispatch')
class MemoryDetail(TemplateView):
  model = Memory
  template_name = "memory_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["memory"] = Memory.objects.get(pk=kwargs["pk"])
    return context

@method_decorator(login_required, name='dispatch')
class JournalCreate(CreateView):
  model = Journal
  fields = ['name', 'birthdate']
  template_name = "journal_create.html"
  success_url = "/journals/"

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
  # Add redirect to users journals
  # def get_success_url(self):
  #   return reverse("")


class RegisterView(View):
  
  def get(self, request):
    form = UserCreationForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)

  def post(self, request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect("home")
    else:
      context = {"form": form}
      return render(request, "registration/register.html", context)


# @method_decorator(login_required, name='dispatch')
# class MemoryCreate(CreateView):
#   model = Memory
#   fields = ['title', 'content', 'is_public', 'photo', 'journal']
#   template_name = "memory_create.html"
  
#   def form_valid(self, form):
#     form.instance.user = self.request.user
#     return super().form_valid(form)
  
#   def get_success_url(self):
#     return reverse("memory_detail", kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class MemoryCreate(View):
  def get(self, request):
      context = {'journals': Journal.objects.all()}
      return render(request, 'memory_create.html', context)

  def post(self, request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    is_public = request.POST.get('is_public')
    if is_public == 'on':
      is_public = True
    else:
      is_public = False
    
    # photo = request.FILES['photo']


    journal = Journal.objects.get(pk=request.POST.get('journal'))
    new_memory = Memory.objects.create(title=title, content=content, is_public=is_public, journal=journal)
    return redirect('memory_detail', pk=new_memory.id)



@method_decorator(login_required, name='dispatch')
class MemoryUpdate(UserPassesTestMixin, UpdateView):
  model = Memory
  fields = ['title', 'content', 'is_public']
  template_name = "memory_update.html"

  def test_func(self):
    memory = get_object_or_404(Memory, pk = self.kwargs["pk"])
    return self.request.user == memory.journal.user
    
  # def form_valid(self, form):
  #   form.instance.user = self.request.user
  #   return super().form_valid(form)

  def get_success_url(self):
    return reverse("memory_detail", kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class JournalDetail(UserPassesTestMixin, TemplateView):
  model = Journal
  template_name = "journal_detail.html"

  def test_func(self):
    journal = get_object_or_404(Journal, pk = self.kwargs["pk"])
    return self.request.user == journal.user
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["journal"] = Journal.objects.get(pk=kwargs["pk"])
    return context


@method_decorator(login_required, name='dispatch')
class MemoryDelete(UserPassesTestMixin, DeleteView):
  model = Memory
  template_name = "memory_delete_confirmation.html"
  # success_url = "/journals/"

  def test_func(self):
    memory = get_object_or_404(Memory, pk = self.kwargs["pk"])
    return self.request.user == memory.journal.user

  def get_success_url(self):
    return reverse("journal_detail", kwargs={'pk': self.object.journal.pk})

@method_decorator(login_required, name='dispatch')
class JournalDelete(UserPassesTestMixin, DeleteView):
  model = Journal
  template_name = "journal_delete_confirmation.html"
  success_url = "/journals/"

  def test_func(self):
    journal = get_object_or_404(Journal, pk = self.kwargs["pk"])
    return self.request.user == journal.user

@method_decorator(login_required, name='dispatch')
class JournalList(TemplateView):
  template_name = "journal_list.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    if user != None:
      context["journals"] = Journal.objects.filter(user=self.request.user)
      return context
    else:
      return redirect('/')

@method_decorator(login_required, name='dispatch')
class JournalUpdate(UserPassesTestMixin, UpdateView):
  model = Journal
  fields = ['name', 'birthdate']
  template_name = "journal_update.html"

  def test_func(self):
    journal = get_object_or_404(Journal, pk = self.kwargs["pk"])
    return self.request.user == journal.user

  # def form_valid(self, form):
  #   form.instance.user = self.request.user
  #   return super().form_valid(form)
  
  def get_success_url(self):
    return reverse("journal_detail", kwargs={'pk': self.object.pk})

class AlbumList(TemplateView):
  template_name = "album_list.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    if user != None:
      context["albums"] = Album.objects.filter(user=self.request.user)
      return context
    else:
      return redirect('/')

class PhotoDetail(TemplateView):
  model = Photo
  template_name = "photo_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["photo"] = Photo.objects.get(pk=kwargs["pk"])
    return context

class AlbumDetail(TemplateView):
  model = Album
  template_name = "album_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["album"] = Album.objects.get(pk=kwargs["pk"])
    return context


class AlbumCreate(CreateView):
  model = Album
  fields = ['title', 'description']
  template_name = "album_create.html"
  success_url = "/albums/"

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class AlbumUpdate(UserPassesTestMixin, UpdateView):
  model = Album
  fields = ['title', 'description']
  template_name = "album_update.html"

  def test_func(self):
    album = get_object_or_404(Album, pk = self.kwargs["pk"])
    return self.request.user == album.user

  def get_success_url(self):
    return reverse("album_detail", kwargs={'pk': self.object.pk})

class AlbumDelete(UserPassesTestMixin, DeleteView):
  model = Album
  template_name = "album_delete_confirmation.html"
  success_url = "/albums/"

  def test_func(self):
    album = get_object_or_404(Album, pk = self.kwargs["pk"])
    return self.request.user == album.user

class PhotoCreate(CreateView):
  model = Photo
  fields = ['album', 'title', 'description', 'is_public', 'picture']
  template_name = "photo_create.html"
  
  def get_success_url(self):
    return reverse("photo_detail", kwargs={'pk': self.object.pk})

class PhotoUpdate(UserPassesTestMixin, UpdateView):
  model = Photo
  fields = ['album', 'title', 'description', 'is_public', 'picture']
  template_name = "photo_update.html"

  def test_func(self):
    photo = get_object_or_404(Photo, pk = self.kwargs["pk"])
    return self.request.user == photo.album.user

  def get_success_url(self):
    return reverse("photo_detail", kwargs={'pk': self.object.pk})

class PhotoDelete(UserPassesTestMixin, DeleteView):
  model = Photo
  template_name = "photo_delete_confirmation.html"
  success_url = "/albums/"

  def test_func(self):
    photo = get_object_or_404(Photo, pk = self.kwargs["pk"])
    return self.request.user == photo.album.user