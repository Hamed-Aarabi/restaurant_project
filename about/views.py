from django.shortcuts import render
from django.views.generic import View
from .models import About


class AboutView(View):
    def get(self,request):
        query = About.objects.all().last()
        return render(request, 'about/about.html', {'query':query})



