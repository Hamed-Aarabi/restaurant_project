from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add-to-cart', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:id>', views.RemoveItemCartView.as_view(), name='remove_from_cart'),
    path('create-order', views.CreateOrderView.as_view(), name='create_order'),
    path('order-detail/<int:id>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-payment/<int:id>', views.PaymentView.as_view(), name='order_payment'),
]