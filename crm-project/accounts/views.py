from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Product, Customer, Order
from .forms import CreateCustomerForm, OrderForm, ProductForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, admin_required
# Create your views here.


@admin_required
@login_required(login_url='login')
def dashboard(request):
    order_list = Order.objects.all()
    total_order = order_list.count()
    completed_order = order_list.filter(status='Completed').count()
    pending_order = order_list.filter(status='Pending').count()
    customer_list = Customer.objects.all()
    total_customer = customer_list.count()
    last5_order = order_list.order_by('-status')[0:5]

    context = {
        'total_order': total_order,
        'completed_order': completed_order,
        'pending_order': pending_order,
        'total_customer': total_customer,
        'customer_list': customer_list,
        'last5_order': last5_order,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def profile(request):
    if request.user.is_staff:
        return redirect('dashboard')
    context = {

    }
    return render(request, 'customers/profile.html', context)

@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')



def create_account(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # Added username after video because of error returning customer name if not added
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )

            messages.success(request, 'Account was created for ' + user.username)

            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'accounts/create_account.html', context)


@admin_required
@login_required(login_url='login')
def products(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'accounts/products.html', context)


# @admin_required
# @login_required(login_url='login')
# def create_customer(request):
#     if request.method == 'POST':
#         form = CreateCustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = CreateCustomerForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'accounts/create_customer.html', context)

@admin_required
@login_required(login_url='login')
def customer_info(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    # total_orders = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'my_filter': my_filter,
    }
    return render(request, 'accounts/customer_info.html', context)


@admin_required
@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products')
    else:
        form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/create_product.html', context)


@admin_required
@login_required(login_url='login')
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'action': 'create',
    }
    return render(request, 'accounts/order_form.html', context)


@admin_required
@login_required(login_url='login')
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        prev_page = request.POST.get('prev_page')
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(prev_page)

    context = {
        'form': form,
        'action': 'update',
    }
    return render(request, 'accounts/order_form.html', context)
