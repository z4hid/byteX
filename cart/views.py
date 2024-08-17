from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from product.models import Product

from django.http import JsonResponse


# This function handles the adding of products to the cart
# It takes in the HTTP request and the product ID as parameters
# It initializes a new instance of the Cart class with the request object
# It then calls the add method of the cart object, passing in the product ID
# Finally, it renders the 'cart/partials/menu_cart.html' template and returns the response
def add_to_cart(request, product_id):
    """
    Handles the adding of products to the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponse: The rendered 'cart/partials/menu_cart.html' template.
    """
    # Initialize a new instance of the Cart class with the request object
    cart = Cart(request)

    # Call the add method of the cart object, passing in the product ID
    cart.add(product_id)

    # Render the 'cart/partials/menu_cart.html' template and return the response
    return render(request, 'cart/partials/menu_cart.html')


# This function handles the rendering of the cart page
# It takes in the HTTP request as a parameter
# It simply renders the 'cart/cart.html' template and returns the response
def cart(request):
    """
    Handles the rendering of the cart page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'cart/cart.html' template.
    """
    # Render the 'cart/cart.html' template and return the response
    return render(request, 'cart/cart.html')


# This function handles the rendering of the success page after a successful purchase
# It takes in the HTTP request as a parameter
# It simply renders the 'cart/success.html' template and returns the response
def success(request):
    """
    Handles the rendering of the success page after a successful purchase.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'cart/success.html' template.
    """
    return render(request, 'cart/success.html')


# This function handles the updating of the cart
# It takes in the HTTP request, the product ID, and the action as parameters
# It initializes a new instance of the Cart class with the request object
# It then checks the action parameter and calls the add method of the cart object accordingly
# It retrieves the product object with the given product ID
# It retrieves the quantity of the product in the cart
# If the quantity is not None, it creates a dictionary with the product information and the quantity
# Finally, it renders the 'cart/partials/cart_item.html' template with the item dictionary as context and returns the response
def update_cart(request, product_id, action):
    """
    Handles the updating of the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to update in the cart.
        action (str): The action to perform on the product in the cart. Can be 'increment' or 'decrement'.

    Returns:
        HttpResponse: The rendered 'cart/partials/cart_item.html' template with the updated item dictionary as context.
        JsonResponse: An error response if the action is invalid, the product does not exist, or an exception occurs.
    """
    try:
        # Initialize a new instance of the Cart class with the request object
        cart = Cart(request)

        # Check the action parameter and call the add method of the cart object accordingly
        if action == 'increment':
            cart.add(product_id, 1, True)
        elif action == 'decrement':
            cart.add(product_id, -1, True)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        # Retrieve the product object with the given product ID
        product = get_object_or_404(Product, pk=product_id)

        # Retrieve the quantity of the product in the cart
        quantity = cart.get_item(product_id)

        if quantity:
            quantity = quantity['quantity']

            # Create a dictionary with the product information and the quantity
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'image': product.image.url,
                    'get_thumbnail': product.get_thumbnail(),
                    'price': product.price,
                },
                'total_price': product.price * quantity,
                'quantity': quantity
            }
        else:
            item = None

        # Render the 'cart/partials/cart_item.html' template with the item dictionary as context and return the response
        response = render(request, 'cart/partials/cart_item.html', {'item': item})
        response['HX-Trigger'] = 'update-menu-cart' 
        return response

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# This function handles the rendering of the checkout page
# It takes in the HTTP request as a parameter
# It retrieves
