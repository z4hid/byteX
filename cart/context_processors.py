from .cart import Cart


def cart(request):
    """
    Returns a dictionary containing the user's cart.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        dict: A dictionary with a single key 'cart' containing the user's Cart instance.
    """
    return {'cart': Cart(request)}