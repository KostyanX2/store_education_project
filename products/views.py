from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from users.models import User
from  django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    context = {
        "title": "STORE",
    }
    return render(request, "products/index.html", context)


def products(request, category_id=None, page_number=1):
    products_ = Product.objects.filter(category__id=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(products_, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        "title": "Store - Каталог",
        "categories": ProductCategory.objects.all(),
        "products": products_paginator,
    }

    return render(request, "products/products.html", context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)


    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def basket_remove(request, basket_id):
    basket_item = Basket.objects.filter(id=basket_id, user=request.user).first()
    if basket_item:
        basket_item.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
