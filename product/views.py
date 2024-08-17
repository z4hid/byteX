from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review


# Create your views here.
def product(request, slug):
    """
    Renders the product page and handles the submission of a new review.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the product.

    Returns:
        HttpResponse: The rendered product page if no review is submitted.
        HttpResponseRedirect: The product page with the new review if a review is submitted.
    """
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating = request.POST.get('rating', 4)
        content  = request.POST.get('content', '')
        if content:
            reviews = Review.objects.filter(product=product, created_by=request.user)
            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review  = Review.objects.create(product=product, 
                                                rating=rating, 
                                                content=content,
                                                created_by=request.user)
            
            return redirect('product', slug=slug)
        
    return render(request, 'product/product.html', {'product': product})