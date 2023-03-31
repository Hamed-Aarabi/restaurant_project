from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
from menu.models import Food


class HomeView(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['foods'] = Food.objects.all()
        return context