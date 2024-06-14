from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from product.models import Product, Category
from .forms import SignupForm
from order.models import Order

# Create your views here.
def frontpage(request):
    products = Product.objects.all()[0:8] # Get 8 Products from the database
    return render(request, 'core/home.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    active_category = request.GET.get('category', '')
    if active_category:
        products = products.filter(category__slug=active_category)
        
    query = request.GET.get('query', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        
    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    }
    return render(request, 'core/shop.html', context)

@login_required
def myaccount(request):
    # Retrieve orders associated with the current user
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders
    }
    
    return render(request, 'core/myaccount.html', context)

@login_required
def edit_myaccount(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('myaccount')
    return render(request, 'core/edit_myaccount.html')