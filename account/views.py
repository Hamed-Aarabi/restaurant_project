import uuid
from random import randint
from .mixins import ClientLoginMixin
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, ListView, DeleteView
from .forms import OtpForm, OtpCreationForm, LoginForm, ClientChangeForm, AddressForm
from .models import Client, Otp, Address
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


class ClientCreationView(FormView):
    template_name = 'account/client_creation.html'
    form_class = OtpCreationForm
    success_url = reverse_lazy('account:client-verification')

    def form_valid(self, form):
        cd = form.cleaned_data
        uuid_otp = uuid.uuid4()
        otp_code_create = randint(1000, 9999)
        print(otp_code_create)
        self.request.session['phone'] = cd['phone']
        self.request.session[self.request.session['phone']] = str(uuid_otp)
        Otp.objects.create(phone=cd['phone'], password=cd['password1_otp'], token=str(uuid_otp),
                           otp_code=otp_code_create)
        return super(ClientCreationView, self).form_valid(form)


class ClientVerificationView(FormView):
    template_name = 'account/client_verification.html'
    form_class = OtpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        cd = form.cleaned_data
        user = Otp.objects.get(token=self.request.session[self.request.session['phone']])
        if not abs(datetime.datetime.now().second - user.otp_create_at.second) > 10:
            if Otp.objects.filter(otp_code=cd['otp_input'], token=self.request.session[self.request.session['phone']],
                                  expired=False).exists():
                new_user = Client.objects.create_user(phone=user.phone, password=user.password)
                user.expired = True
                user.save()
                del self.request.session[self.request.session['phone']]
                del self.request.session['phone']
                self.request.session.modified = True
                login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            user.expired = True
            user.save()
            return redirect('account:client-verification')
        return super(ClientVerificationView, self).form_valid(form)

    # def form_invalid(self, form):
    #     cd = form.cleaned_data
    #     user = Otp.objects.get(token=self.request.session[self.request.session['phone']])
    #     if abs(datetime.datetime.now().second - user.otp_create_at.second) > 10:
    #         user.expired = True
    #         user.save()
    #         return redirect('account:client-verification')
    #     return super(ClientVerificationView, self).form_valid(form)


def client_verification_resend(request):
    user = Otp.objects.get(token=request.session[request.session['phone']])
    otp_code_resend = randint(1000, 9999)
    print(otp_code_resend)
    user.otp_code = otp_code_resend
    user.expired = False
    user.save()
    return redirect('account:client-verification')


class ClientLoginView(ClientLoginMixin, FormView):
    template_name = 'account/client_login.html'
    form_class = LoginForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        login(self.request, user)
        next_page = self.request.GET.get('next')
        if next_page:
            return redirect(next_page)
        return super(ClientLoginView, self).form_valid(form)

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page:
            self.success_url = next_page
        else:
            self.success_url=reverse_lazy('home')
        return super(ClientLoginView, self).get_success_url()


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/client_update.html'
    form_class = ClientChangeForm
    model = Client
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Client, id=request.user.id)
        if self.kwargs.get('pk') != user.id:
            return redirect('account:client-update', user.id)
        return super(ClientUpdateView, self).get(request, *args, **kwargs)

class AddAddressView(FormView):
    template_name = 'account/address_add.html'
    form_class = AddressForm

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page:
            self.success_url = next_page
        return super(AddAddressView, self).get_success_url()

    def form_valid(self, form):
        cd = form.cleaned_data
        Address.objects.create(client=self.request.user, state=cd['state'], city=cd['city'], address=cd['address'])
        return super(AddAddressView, self).form_valid(form)

class AddressListView(ListView):
    template_name = 'account/address_list.html'
    context_object_name = 'addresses'

    def get(self, request, *args, **kwargs):
        user = Client.objects.get(id=request.user.id)
        if self.kwargs.get('pk') != user.id:
            return redirect('account:client-addresses', user.id)
        return super(AddressListView, self).get(request, *args, **kwargs)


    def get_queryset(self, **kwargs):
        user = Client.objects.get(id=self.kwargs.get('pk'))
        queryset = user.client_address.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AddressListView, self).get_context_data(**kwargs)
        allow_add = True
        user = Client.objects.get(id=self.kwargs.get('pk'))
        queryset = user.client_address.all().count()
        context['address_count'] = queryset
        if queryset >= 4 :
            allow_add = False
        context['allow_add'] = allow_add
        return context


class AddressEditView(UpdateView):
    template_name = 'account/address_edit.html'
    model = Address
    fields = '__all__'

    def get_object(self, queryset=None):
        queryset = Address.objects.get(client_id=self.kwargs.get('pk'), id=self.kwargs.get('address_id'))
        return queryset

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page:
            self.success_url = next_page
        return super(AddressEditView, self).get_success_url()

class AddressDeleteView(DeleteView):
    template_name = 'account/address_delete.html'
    model = Address

    def get_object(self, queryset=None):
        queryset = Address.objects.get(client_id=self.kwargs.get('pk'), id=self.kwargs.get('address_id'))
        return queryset

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page:
            self.success_url = next_page
        return super(AddressDeleteView, self).get_success_url()


def logout_request(request):
    logout(request)
    return redirect('home')
