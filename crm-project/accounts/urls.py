from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('create-customer/', views.create_customer, name='create_customer'),
    path('create-order/', views.create_order, name='create_order'),
    path('create-product/', views.create_product, name='create_product'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
]