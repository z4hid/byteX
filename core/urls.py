from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from core.views import frontpage, shop, signup, myaccount, edit_myaccount
from product.views import product


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('myaccount/', myaccount, name='myaccount'),
    path('myaccount/edit', edit_myaccount, name='edit_myaccount'),
    path('shop/', shop, name='shop'),
        path('shop/<slug:slug>/', product, name='product'),

]