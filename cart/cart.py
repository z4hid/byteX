from django.conf import settings

from product.models import Product

class Cart(object):
    def __init__(self, request):
        """
        Initializes a new instance of the Cart class.

        Args:
            request (HttpRequest): The HTTP request object.

        Initializes the session attribute with the session from the request object.
        Retrieves the cart from the session using the CART_SESSION_ID setting.
        If the cart is not found, creates a new empty cart in the session.
        Sets the cart attribute to the retrieved or created cart.

        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def __iter__(self):
        """
        Returns an iterator over the items in the cart.

        Yields:
            dict: A dictionary representing an item in the cart. The dictionary contains the following keys:
                - 'product' (Product): The product object associated with the item.
                - 'quantity' (int): The quantity of the product in the item.
                - 'total_price' (float): The total price of the item, calculated as the product price multiplied by the quantity.

        This method retrieves the product objects associated with each item in the cart and calculates the total price of each item. It then yields each item as a dictionary.

        Note:
            The 'product' key in each item dictionary is populated by retrieving the product object from the database using the product ID stored in the item dictionary.

        """
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity']) / 100

            yield item
    
    def __len__(self):
        """
        Returns the total quantity of items in the cart.

        :return: An integer representing the total quantity of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        """
        Save the cart data to the session.

        This function saves the cart data to the session using the `CART_SESSION_ID` setting as the key.
        It updates the `modified` flag of the session to indicate that the session has been modified.

        Parameters:
            None

        Returns:
            None
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def add(self, product_id, quantity=1, update_quantity=False):
        """
        Adds a product to the cart or updates its quantity.

        Args:
            product_id (str): The ID of the product to add or update.
            quantity (int, optional): The quantity of the product to add or update. Defaults to 1.
            update_quantity (bool, optional): Whether to update the quantity of an existing product. 
                If False, adds a new product to the cart. Defaults to False.

        Returns:
            None
        """
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
            
        self.save()
    
    def remove(self, product_id):
        """
        Removes a product from the cart.

        Args:
            product_id (str): The ID of the product to remove from the cart.

        Returns:
            None
        """
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def clear(self):
        """
        Clears the cart session by deleting the cart session ID from the session dictionary and setting the modified flag to True.

        This function is used to remove all items from the cart and clear the cart session. It deletes the cart session ID from the session dictionary using the `CART_SESSION_ID` setting as the key. It then sets the modified flag of the session to True to indicate that the session has been modified.

        Parameters:
            None

        Returns:
            None
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    
    def get_total_cost(self):
        """
        Calculates the total cost of all items in the cart.

        This function iterates over the keys of the cart dictionary and retrieves the corresponding product object using the product ID. It then calculates the total cost of each item by multiplying the product price with the quantity and sums up all the costs. The result is returned as a float.

        Returns:
            float: The total cost of all items in the cart.
        """
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return float(sum(item['product'].price * item['quantity'] for item in self.cart.values()))
    
    def get_item(self, product_id):
        """
        Retrieves the item with the given product ID from the cart.

        Args:
            product_id (str): The ID of the product to retrieve.

        Returns:
            dict or None: The item with the given product ID, or None if the product ID is not in the cart.
            The item is represented as a dictionary with the following keys:
                - 'quantity' (int): The quantity of the product in the item.
                - 'id' (str): The ID of the product.
        """
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None