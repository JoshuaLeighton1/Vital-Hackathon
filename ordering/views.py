from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Product, Order, EmployeeProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def dashboard(request):
    products = Product.objects.filter(stock_quantity__gt=0)
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)

    #Calculate cart count for the UI Badge
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())


    context = {
        'products': products,
        'profile': profile,
        'recent_orders': cart_count
    }
    return render(request, 'ordering/dashboard.html', context)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('dashboard')

        # Retrieve or initialize the session cart
        cart = request.session.get('cart', {})
        
        # Session keys must be strings
        pid = str(product_id)
        cart[pid] = cart.get(pid, 0) + quantity
        
        request.session['cart'] = cart
        messages.success(request, f"Added {quantity}x {product.name} to cart.")
        
    return redirect('dashboard')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    
    cart_items = []
    cart_total = Decimal('0.00')
    
    # Build cart items for the UI and calculate total
    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        cost = product.price * int(qty)
        cart_total += cost
        cart_items.append({
            'product': product,
            'quantity': int(qty),
            'cost': cost
        })
        
    if request.method == 'POST':
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('dashboard')
            
        # ERROR HANDLING: Atomic transaction ensures partial orders don't process if something fails
        with transaction.atomic():
            profile = EmployeeProfile.objects.select_for_update().get(user=request.user)
            
            if profile.available_balance < cart_total:
                messages.error(request, "Insufficient allowance balance for this order.")
                return redirect('checkout')
                
            for item in cart_items:
                product = Product.objects.select_for_update().get(id=item['product'].id)
                qty = item['quantity']
                
                if product.stock_quantity < qty:
                    messages.error(request, f"Not enough stock for {product.name}. Please adjust your cart.")
                    return redirect('checkout')
                    
                # Deduct stock and create order records
                product.stock_quantity -= qty
                product.save()
                
                Order.objects.create(
                    employee=profile,
                    product=product,
                    quantity=qty,
                    total_cost=item['cost'],
                    status="Confirmed"
                )
                
            # Deduct the total cost from the employee's allowance
            profile.allowance_used += cart_total
            profile.save()
            
            # Clear the session cart
            request.session['cart'] = {}
            messages.success(request, "Checkout successful! Your order has been placed.")
            return redirect('dashboard')
            
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'profile': profile
    }
    return render(request, 'ordering/checkout.html', context)

login_required
def add_dummy_funds(request):
    """A dummy endpoint for the hackathon to demonstrate adding external funds/allowance."""
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '100.00'))
        profile = get_object_or_404(EmployeeProfile, user=request.user)
        
        # Increase their total monthly allowance cap
        profile.monthly_allowance += amount
        profile.save()
        messages.success(request, f"Dummy action: Successfully added R{amount} to your allowance limit!")
        
    return redirect('dashboard')


def register(request):
    # If the user is already logged in, redirect them to the dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            user = form.save()
            
            # Explicitly create their employee profile with the default R500 allowance
            EmployeeProfile.objects.create(user=user)
            
            # Automatically log them in after registering
            login(request, user)
            messages.success(request, f"Welcome to VitalStaff, {user.username}!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})