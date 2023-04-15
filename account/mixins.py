from django.shortcuts import redirect

# This mixin, if user authenticated request to login page return it to home
class ClientLoginMixin:
    def dispatch(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        return super(ClientLoginMixin, self).dispatch(request)


class VerificationValidMixin:
    def dispatch(self, request):
        if not request.session.get(request.session.get('phone')):
            return redirect('account:client-creation')
        return super(VerificationValidMixin, self).dispatch(request)