from django.shortcuts import render, redirect
from django.views.generic import View
from contact_us.models import Message
from .models import About
from contact_us.forms import ContactUsForm


class AboutView(View):
    def get(self, request):
        query = About.objects.all().last()
        form = ContactUsForm()
        return render(request, 'about/about.html', {'query': query, 'form': form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Message.objects.create(name=cd['name'], email=cd['email'], phone=cd['phone'], message=cd['message'])
            return redirect('about:about')
        else:
            form = ContactUsForm()
        return render(request, 'about/about.html', {'form': form})
