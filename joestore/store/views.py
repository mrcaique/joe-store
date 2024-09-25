from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import CreateUserForm
import json
import datetime

def register(request: HttpRequest) -> HttpResponse:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context = {'form': form}
    return render(request, 'account/register.html', context)


def loginPage(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {'form': form}
    return render(request, 'account/login.html', context)


def logoutUser(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


def store(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request: HttpRequest) -> HttpResponse:
    """Create cart for registered user, otherwise create an
    empty cart for non-logged user"""
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )
    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request: HttpRequest) -> JsonResponse:
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')
    return JsonResponse('Payment submitted', safe=False)


@login_required(login_url='login')
def orderHistory(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(customer=request.user.customer, complete=True).order_by('-id')
    context = {'order_history': orders}
    return render(request, 'store/order_history/orderhistory.html', context)


@login_required(login_url='login')
def orderDetails(request: HttpRequest, id: int) -> HttpResponse:
    order = Order.objects.filter(id=id).first()
    orderitems = OrderItem.objects.filter(order=id)
    context = {'order': order, 'order_items': orderitems}
    return render(request, 'store/order_history/orderdetails.html', context)
