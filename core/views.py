from django.shortcuts import render
from product.models import Product

# Create your views here.
def frontpage(request):
    products = Product.objects.all()[0:8] # Get 8 Products from the database
    return render(request, 'core/home.html', {'products': products})