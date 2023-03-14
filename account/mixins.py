from django.shortcuts import redirect


class ClientLoginMixin:
    def dispatch(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        return super(ClientLoginMixin, self).dispatch(request)
