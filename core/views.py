from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from product.models import Product, Category
from .forms import SignupForm
from order.models import Order

# Create your views here.
def frontpage(request):
    """
    Handles the front page view of the application.

    Parameters:
    request (HttpRequest): The current HTTP request.

    Returns:
    HttpResponse: A rendered HTML response for the front page.
    """
    products = Product.objects.all()[0:8] # Get 8 Products from the database
    return render(request, 'core/home.html', {'products': products})

def signup(request):
    """
    Handles the signup view of the application.

    Parameters:
    request (HttpRequest): The current HTTP request.

    Returns:
    HttpResponse: A rendered HTML response for the signup page or a redirect to the homepage upon successful signup.
    """
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
    """
    Handles the shop view of the application.

    Parameters:
    request (HttpRequest): The current HTTP request.

    Returns:
    HttpResponse: A rendered HTML response for the shop page.
    """
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
    """
    Handles the myaccount view of the application.

    Parameters:
    request (HttpRequest): The current HTTP request.

    Returns:
    HttpResponse: A rendered HTML response for the myaccount page.
    """
    # Retrieve orders associated with the current user
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders
    }
    
    return render(request, 'core/myaccount.html', context)

@login_required
def edit_myaccount(request):
    """
    Updates the user's account information based on the request method.
    
    If the request method is POST, it retrieves and updates the user details from the form data,
    saves them to the database, and then redirects to the 'myaccount' page.
    
    If the request method is not POST, it renders the 'core/edit_myaccount.html' template 
    for user input.
    
    Parameters:
        request (HttpRequest): The current HTTP request object containing form data if applicable.
        
    Returns:
        HttpResponseRedirect: Redirects to the 'myaccount' page after successfully updating the account information.
        HttpResponse: Renders the 'core/edit_myaccount.html' template for GET requests, allowing user input and validation.
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('myaccount')
    return render(request, 'core/edit_myaccount.html')