from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Product, Customer, Order
from .forms import CreateCustomerForm, OrderForm, ProductForm
from .filters import OrderFilter
# Create your views here.

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


def products(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'accounts/products.html', context)

def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = CreateCustomerForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/create_customer.html', context)

def customer_info(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    # total_orders = orders.count()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'accounts/customer_info.html', context)


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

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'action': 'create',
    }
    return render(request, 'accounts/order_form.html', context)

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