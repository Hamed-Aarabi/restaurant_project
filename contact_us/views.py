from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import ContactUsForm
from .models import Message


class ContactUsView(FormView):
    template_name = 'contact_us/contact_us.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('contact_us:contact-us')


    def form_valid(self, form):
        cd = form.cleaned_data
        Message.objects.create(name=cd['name'], email=cd['email'], phone=cd['phone'], message=cd['message'])
        return super(ContactUsView, self).form_valid(form)