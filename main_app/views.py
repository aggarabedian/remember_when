from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse


# Imports Models
from .models import Journal, Memory
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

class Home(TemplateView):
  template_name = "home.html"

class About(TemplateView):
  template_name = "about.html"

class JournalList(TemplateView):
  template_name = "journal_list.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["journals"] = Journal.objects.all()
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