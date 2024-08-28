from django.apps import AppConfig


class ProductConfig(AppConfig):
    """
    This class represents the configuration for the 'product' app.

    It inherits from the `AppConfig` class provided by Django.
    """

    # Specify the default field to use for auto-generated primary keys.
    # This setting is used by Django to automatically create primary keys
    # for new models in the 'product' app.
    default_auto_field = 'django.db.models.BigAutoField'

    # Specify the name of the app.
    # This setting is used by Django to identify the 'product' app.
    name = 'product'

