from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView



class HomeView(TemplateView):
    template_name = 'index.html'