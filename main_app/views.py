from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView


# Imports Models
from .models import Journal, Memory
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

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

class MemoryView(TemplateView):
  template_name = "memory.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["memories"] = Memory.objects.all()
    return context