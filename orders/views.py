from cart.cart import Cart
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem

def order_create(request):
    cart = Cart(request)  # Instancia del carrito
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            # Crear la orden con los datos del formulario
            order = form.save()
            
            # Crear los ítems de la orden a partir del carrito
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Vaciar el carrito después de procesar la orden
            cart.clear()
            
            # Redirigir a la página de confirmación de la orden
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    # Renderizar la plantilla para crear una nueva orden
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
