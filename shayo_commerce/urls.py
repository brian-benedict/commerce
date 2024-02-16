from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.create_product, name='create_product'),  # New URL for creating a product
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),  # New URL for editing a product
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    # Add more URLs for user authentication, profile, payment processing, etc.
    path('categories/create/', views.create_category, name='create_category'),


]
