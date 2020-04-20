from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create-account/', views.create_account, name='create_account'),
    path('products/', views.products, name='products'),
    # path('create-customer/', views.create_account, name='create_customer'),
    path('create-order/', views.create_order, name='create_order'),
    path('create-product/', views.create_product, name='create_product'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('customer/<str:pk>/', views.customer_info, name='customer_info'),
]