from cart.cart import Cart
from django.shortcuts import redirect, render
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

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
            
            # Llamar a la tarea asíncrona para enviar el correo de confirmación
            order_created.delay(order.id)

            # Set the order in the session
            request.session['order_id'] = order.id

            # Redirect for payment
            return redirect('payment:process')

    else:
        form = OrderCreateForm()
    
    # Renderizar la plantilla para crear una nueva orden
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


