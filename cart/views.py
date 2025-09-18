from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item, Cart, CartItem

def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts.login')
    
    # Get all carts for the user
    user_carts = Cart.objects.filter(user=request.user)
    
    # Get the selected cart ID from the request
    selected_cart_id = request.GET.get('cart_id')
    
    if selected_cart_id:
        try:
            selected_cart = get_object_or_404(Cart, id=selected_cart_id, user=request.user)
        except:
            selected_cart = None
    else:
        # Default to the first cart if no cart is selected
        selected_cart = user_carts.first()
    
    cart_total = 0
    movies_in_cart = []
    cart_items = []
    
    if selected_cart:
        cart_items = CartItem.objects.filter(cart=selected_cart)
        movies_in_cart = [item.movie for item in cart_items]
        cart_total = sum(item.movie.price * item.quantity for item in cart_items)
    
    template_data = {
        'title': 'Cart',
        'movies_in_cart': movies_in_cart,
        'cart_total': cart_total,
        'user_carts': user_carts,
        'selected_cart': selected_cart,
        'cart_items': cart_items
    }
    
    return render(request, 'cart/index.html', {'template_data': template_data})

@login_required
def add(request, id):
    movie = get_object_or_404(Movie, id=id)
    
    # Get cart name from the form
    cart_name = request.POST.get('cart_name', 'Cart 1')
    
    # Get or create the cart
    cart, created = Cart.objects.get_or_create(
        name=cart_name,
        user=request.user,
        defaults={'name': cart_name}
    )
    
    # Get or create the cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        movie=movie,
        defaults={'quantity': int(request.POST['quantity'])}
    )
    
    if not created:
        # If item already exists, update the quantity
        cart_item.quantity += int(request.POST['quantity'])
        cart_item.save()
    
    messages.success(request, f'Added {movie.name} to {cart.name}')
    return redirect('cart.index')

@login_required
def clear(request):
    cart_id = request.GET.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, f'Cleared {cart.name}')
    return redirect('cart.index')

@login_required
def purchase(request):
    cart_id = request.GET.get('cart_id')
    if not cart_id:
        messages.error(request, 'No cart selected for purchase')
        return redirect('cart.index')
    
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.error(request, 'Cart is empty')
        return redirect('cart.index')
    
    # Calculate total
    cart_total = sum(item.movie.price * item.quantity for item in cart_items)
    
    # Create order
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    
    # Create order items
    for cart_item in cart_items:
        item = Item()
        item.movie = cart_item.movie
        item.price = cart_item.movie.price
        item.order = order
        item.quantity = cart_item.quantity
        item.save()
    
    # Clear the cart
    cart_items.delete()
    
    template_data = {
        'title': 'Purchase confirmation',
        'order_id': order.id,
        'cart_name': cart.name
    }
    
    return render(request, 'cart/purchase.html', {'template_data': template_data})

@login_required
def create_cart(request):
    if request.method == 'POST':
        cart_name = request.POST.get('cart_name')
        if cart_name:
            cart, created = Cart.objects.get_or_create(
                name=cart_name,
                user=request.user
            )
            if created:
                messages.success(request, f'Created cart: {cart_name}')
            else:
                messages.error(request, f'Cart "{cart_name}" already exists')
        else:
            messages.error(request, 'Cart name is required')
    
    return redirect('cart.index')
