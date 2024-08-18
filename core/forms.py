# Import the necessary modules from Django and the Python standard library
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Define a new form class called SignupForm which inherits from UserCreationForm
class SignupForm(UserCreationForm):
    # Define a field for the first name with a maximum length of 50 characters
    first_name = forms.CharField(max_length=50, required=True)
    # Define a field for the last name with a maximum length of 50 characters
    last_name  = forms.CharField(max_length=50, required=True)
    # Define a field for email with a maximum length of 255 characters
    email = forms.EmailField(max_length=255, required=True)

    # Define a Meta inner class to specify additional options for the form
    class Meta:
        # Set the model for the form to the Django User model
        model = User
        # Specify the fields to be included in the form.
        # Include the username, first name, last name, email, password1, and password2 fields.
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]
