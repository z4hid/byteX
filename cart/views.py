from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from product.models import Product

from django.http import JsonResponse

def add_to_cart(request, product_id):
    cart = Cart(request)

    cart.add(product_id)
    return render(request, 'cart/partials/menu_cart.html')

def cart(request):
    # cart = Cart(request)
    # print(cart)
    # for item in cart:
    #     print(item)
    return render(request, 'cart/cart.html')

def success(request):
    return render(request, 'cart/success.html')

def update_cart(request, product_id, action):
    try:
        cart = Cart(request)
        
        if action == 'increment':
            cart.add(product_id, 1, True)
        elif action == 'decrement':
            cart.add(product_id, -1, True)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        product = get_object_or_404(Product, pk=product_id)

        quantity = cart.get_item(product_id)
        
        if quantity:
            quantity = quantity['quantity']

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

        response = render(request, 'cart/partials/cart_item.html', {'item': item})
        response['HX-Trigger'] = 'update-menu-cart' 
        return response

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')