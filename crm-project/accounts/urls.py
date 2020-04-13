from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
]