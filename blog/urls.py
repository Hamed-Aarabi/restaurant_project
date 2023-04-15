from django.urls import path
from . import views



app_name = 'blog'
urlpatterns = [
    path('', views.BlogView.as_view(), name = 'blogs'),
    path('<int:pk>', views.BlogDetailView.as_view(), name = 'detail'),
    path('like/<int:pk>', views.like_blog, name = 'like')
]