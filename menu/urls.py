from django.urls import path
from  . import views


app_name = 'menu'
urlpatterns = [
    path('',views.FoodMenuView.as_view(), name='menu'),
    path('detail/<int:pk>', views.FoodDetailView.as_view(), name='food-detail'),
    path('manage-orders', views.ManageOrdersView.as_view(), name='manage-orders'),
    path('manage-orders/delete/<int:pk>', views.DeleteOrderView.as_view(), name='order-delete'),
]