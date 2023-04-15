from django.shortcuts import render, redirect
from django.views.generic import View
from contact_us.forms import ContactUsForm
from contact_us.models import Message
from menu.models import Food


class HomeView(View):

    def get(self, request):
        foods = Food.objects.all()
        form = ContactUsForm()
        return render(request, 'index.html', {'foods': foods, 'form': form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Message.objects.create(name=cd['name'], email=cd['email'], phone=cd['phone'], message=cd['message'])
            return redirect('home')
        else:
            form = ContactUsForm()
        return render(request, 'index.html', {'form': form})
