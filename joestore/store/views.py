from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def store(request) -> HttpResponse:
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request) -> HttpResponse:
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request) -> HttpResponse:
    context = {}
    return render(request, 'store/checkout.html', context)