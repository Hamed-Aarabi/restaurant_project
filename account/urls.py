from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('client-cration', views.ClientCreationView.as_view(), name='client-creation'),
    path('client-verification', views.ClientVerificationView.as_view(), name='client-verification'),
    path('client-verification-resend-code', views.client_verification_resend, name='client-verification_resend'),
    path('client-login', views.ClientLoginView.as_view(), name='client-login'),
    path('client-logout', views.logout_request, name='client-logout'),
    path('client-update/<int:pk>', views.ClientUpdateView.as_view(), name='client-update'),
    path('client-address/<int:pk>', views.AddressListView.as_view(), name='client-addresses'),
    path('client-address-add/<int:pk>', views.AddAddressView.as_view(), name='client-address-add'),
    path('client-address-update/<int:pk>/<int:address_id>', views.AddressEditView.as_view(), name='client-address-update'),
    path('client-address-delete/<int:pk>/<int:address_id>', views.AddressDeleteView.as_view(), name='client-address-delete'),


]