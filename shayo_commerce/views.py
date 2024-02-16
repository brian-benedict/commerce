from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem, Order, Address, Payment, Review, OrderItem
from .forms import AddressForm, ReviewForm

def home(request):
    products = Product.objects.all()[:10]  # Display the first 10 products on the home page
    return render(request, 'home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
            return redirect('product_detail', product_id=product_id)

    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews, 'review_form': review_form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
    return redirect('cart')

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    address_form = AddressForm()
    
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save()
            order = Order.objects.create(user=request.user, shipping_address=address)
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            cart_items.delete()
            return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items, 'address_form': address_form})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

# Additional views for user profile, order history, and payment processing can be added here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product

# @login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

# @login_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user != product.user:
        # Redirect or show error message indicating user doesn't have permission to edit this product
        pass
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})



from django.shortcuts import render, redirect
from .forms import CategoryForm

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list or any other page
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})
