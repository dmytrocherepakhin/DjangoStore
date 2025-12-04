from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Product, Cart, CartItem, Order, OrderItem, Review


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'store/product_detail.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Review.objects.create(product=product, user=request.user, content=content)
            return redirect('product_detail', pk=pk)
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum([item.subtotal() for item in items])
    return render(request, 'store/cart_detail.html', {'cart': cart, 'items': items, 'total': total})


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = sum(item.subtotal() for item in items)

    # Створюємо замовлення
    order = Order.objects.create(user=request.user, total_price=total)

    for item in items:
        # Створюємо позицію замовлення
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # 🟢 Зменшуємо залишок товарів
        item.product.quantity -= item.quantity
        item.product.save()

    # Очищаємо кошик
    cart.items.all().delete()

    return render(request, 'store/order_complete.html', {'order': order})
