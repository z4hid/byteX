# This file contains the models for the product and review app.
# Each product has a category, name, slug, description, price, availability, creation date, image, and thumbnail.
# Each review has a product, rating, content, creator, and creation date.

from django.db import models
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.contrib.auth.models import User

# Define the Category model.
# A category has a name and a slug.
class Category(models.Model):
    name = models.CharField(max_length=255)  # The name of the category.
    slug = models.SlugField()  # The slug used in the URL.
    
    class Meta:
        ordering = ('name',)  # Categories are ordered by name.
        verbose_name = 'category'  # The verbose name for a single category.
        verbose_name_plural = 'categories'  # The verbose name for multiple categories.

    def __str__(self):
        return self.name  # Return the name of the category when it is converted to a string.
    

# Define the Product model.
# A product has a category, name, slug, description, price, availability, creation date, image, and thumbnail.
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  # The category of the product.
    name = models.CharField(max_length=255)  # The name of the product.
    slug = models.SlugField()  # The slug used in the URL.
    description = models.TextField(blank=True, null=True)  # The description of the product.
    price = models.DecimalField(max_digits=12, decimal_places=2)  # The price of the product.
    available = models.BooleanField(default=True)  # Whether the product is available.
    created_at = models.DateTimeField(auto_now_add=True)  # The date and time the product was created.
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # The image of the product.
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)  # The thumbnail of the product.

    class Meta:
        ordering = ('-created_at',)  # Products are ordered by creation date in descending order.

    def __str__(self):
        return self.name  # Return the name of the product when it is converted to a string.
    
    def get_display_price(self):
        return self.price  # Return the price of the product.
    
    def get_thumbnail(self):
        if self.image:  # If the product has an image,
            return self.image.url  # return the URL of the image.
        else:  # If the product does not have an image,
            if self.image:  # if there is an image file,
                self.thumbnail = self.make_thumbnail(self.image)  # create a thumbnail from the image.
                self.save()  # save the thumbnail to the database.
                return self.thumbnail.url  # return the URL of the thumbnail.
            else:  # if there is no image file,
                return 'https://via.placeholder.com/240x240.jpg'  # return a placeholder image URL.
            
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)  # Open the image file.
        img.convert('RGB')  # Convert the image to RGB format.
        img.thumbnail(size)  # Create a thumbnail of the specified size.
        thumb_io = BytesIO()  # Create a buffer to store the thumbnail.
        img.save(thumb_io, 'JPEG', quality=85)  # Save the thumbnail to the buffer in JPEG format.
        thumbnail = File(thumb_io, name=image.name)  # Create a Django File object from the thumbnail buffer.
        return thumbnail  # Return the thumbnail.
    
    def get_rating(self):
        reviews_total = 0  # Initialize the total rating of the product to 0.
        
        # Iterate over all reviews of the product and add up the ratings.
        for review in self.reviews.all():
            reviews_total += review.rating
            
            # If there are any reviews, calculate and return the average rating of the product.
            if reviews_total > 0:
                return reviews_total / self.reviews.count()
            
            return 0  # If there are no reviews, return 0 as the rating.
    


# Define the Review model.
# A review has a product, rating, content, creator, and creation date.
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # The product being reviewed.
    rating = models.IntegerField(default=4)  # The rating given to the product.
    content = models.TextField()  # The content of the review.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews' )  # The user who created the review.
    created_at = models.DateTimeField(auto_now_add=True)  # The date and time the review was created.

