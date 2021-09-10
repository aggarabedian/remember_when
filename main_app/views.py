from django.shortcuts import render, redirect
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


# Imports Models
from .models import Journal, Memory
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

class MemoryDetail(TemplateView):
  model = Memory
  template_name = "memory_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["memory"] = Memory.objects.get(pk=kwargs["pk"])
    return context


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


class MemoryCreate(CreateView):
  model = Memory
  fields = ['title', 'content', 'is_public', 'photo', 'journal']
  template_name = "memory_create.html"
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse("memory_detail", kwargs={'pk': self.object.pk})


class MemoryUpdate(UpdateView):
  model = Memory
  fields = ['title', 'content', 'is_public', 'photo']
  template_name = "memory_update.html"
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_success_url(self):
    return reverse("memory_detail", kwargs={'pk': self.object.pk})


class JournalDetail(TemplateView):
  model = Journal
  template_name = "journal_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["journal"] = Journal.objects.get(pk=kwargs["pk"])
    return context


class MemoryDelete(DeleteView):
  model = Memory
  template_name = "memory_delete_confirmation.html"
  success_url = "/journals/"

class JournalDelete(DeleteView):
  model = Journal
  template_name = "journal_delete_confirmation.html"
  success_url = "/journals/"

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
