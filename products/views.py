from django.shortcuts import HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from  django.contrib.auth.decorators import login_required
from common.views import TitleMixin
# Create your views here.



class IndexView(TitleMixin,TemplateView):
    template_name = "products/index.html"
    title = "STORE"


class ProductsListView(TitleMixin,ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 3
    title = "Store - Каталог"
    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id= category_id) if category_id else queryset
    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['selected_category'] = self.kwargs.get('category_id')
        return context

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
